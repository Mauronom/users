from concurrent.futures import ThreadPoolExecutor, as_completed
from django.core.management.base import BaseCommand
from django.db import connection
from investigation.models import ClueModel
from hex.investigation.domain import RateLimitError
from hex.investigation.app import ClassifyClue, ExtractContact
from hex.investigation.infra.buses import i_bus

BATCH_SIZE = 5


def _process_clue(clue_obj):
    try:
        if clue_obj.type == "entity":
            i_bus.dispatch(ExtractContact(clue_text=clue_obj.clue))
        else:
            i_bus.dispatch(ClassifyClue(clue_text=clue_obj.clue))
        clue_obj.refresh_from_db()
        return ("done", clue_obj)
    except RateLimitError:
        clue_obj.status = "pending"
        clue_obj.save(update_fields=["status"])
        return ("rate_limit", clue_obj)
    except Exception as exc:
        clue_obj.status = "error"
        clue_obj.save(update_fields=["status"])
        return ("error", clue_obj, exc)
    finally:
        connection.close()


class Command(BaseCommand):
    help = "Run investigation agents on pending clues"

    def add_arguments(self, parser):
        parser.add_argument("n", nargs="?", type=int, default=10)
        parser.add_argument("--scouts-only", action="store_true")
        parser.add_argument("--entities-only", action="store_true")

    def handle(self, *args, **options):
        n = options["n"]
        scouts_only = options["scouts_only"]
        entities_only = options["entities_only"]

        stale = ClueModel.objects.filter(status="investigating").update(status="pending")
        if stale:
            self.stdout.write(f"Reset {stale} stale 'investigating' clue(s) to pending.")

        qs = ClueModel.objects.filter(status="pending").order_by("-score", "-times_returned")
        if scouts_only:
            qs = qs.filter(type="scout")
        elif entities_only:
            qs = qs.filter(type="entity")

        pending = list(qs[:n])
        if not pending:
            self.stdout.write("No pending clues.")
            return

        self.stdout.write(f"Processing {len(pending)} clue(s) in batches of {BATCH_SIZE}...")
        done = errors = 0
        rate_limited = False

        batches = [pending[i:i + BATCH_SIZE] for i in range(0, len(pending), BATCH_SIZE)]

        for batch in batches:
            if rate_limited:
                break

            for clue_obj in batch:
                self.stdout.write(f"\n→ {clue_obj.clue} (score={clue_obj.score}, type={clue_obj.type})")
                clue_obj.status = "investigating"
                clue_obj.save(update_fields=["status"])

            with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
                futures = {executor.submit(_process_clue, clue_obj): clue_obj for clue_obj in batch}
                for future in as_completed(futures):
                    result = future.result()
                    outcome, clue_obj = result[0], result[1]
                    if outcome == "done":
                        self.stdout.write(f"  done: {clue_obj.clue} (type={clue_obj.type}, status={clue_obj.status})")
                        done += 1
                    elif outcome == "rate_limit":
                        self.stdout.write(self.style.WARNING(f"  Rate limited on {clue_obj.clue}. Stopping after this batch."))
                        rate_limited = True
                    elif outcome == "error":
                        self.stdout.write(self.style.ERROR(f"  Error on {clue_obj.clue}: {result[2]}"))
                        errors += 1

        self.stdout.write(f"\nDone: {done} processed, {errors} error(s).")
