from django.core.management.base import BaseCommand
from investigation.models import ClueModel
from hex.investigation.domain import RateLimitError
from hex.investigation.app import ClassifyClue, ExtractContact
from hex.investigation.infra.buses import i_bus


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

        self.stdout.write(f"Processing {len(pending)} clue(s)...")
        done = errors = 0

        for clue_obj in pending:
            self.stdout.write(f"\n→ {clue_obj.clue} (score={clue_obj.score}, type={clue_obj.type})")
            clue_obj.status = "investigating"
            clue_obj.save(update_fields=["status"])

            try:
                if clue_obj.type == "entity":
                    i_bus.dispatch(ExtractContact(clue_text=clue_obj.clue))
                else:
                    i_bus.dispatch(ClassifyClue(clue_text=clue_obj.clue))
                clue_obj.refresh_from_db()
                self.stdout.write(f"  done (type={clue_obj.type}, status={clue_obj.status})")
                done += 1
            except RateLimitError:
                clue_obj.status = "pending"
                clue_obj.save(update_fields=["status"])
                self.stdout.write(self.style.WARNING("  Rate limited. Stopping. Re-run later."))
                break
            except Exception as e:
                clue_obj.status = "error"
                clue_obj.save(update_fields=["status"])
                self.stdout.write(self.style.ERROR(f"  Error: {e}"))
                errors += 1

        self.stdout.write(f"\nDone: {done} processed, {errors} error(s).")
