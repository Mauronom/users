from hex.mailing.infra.buses import CommandBus


def init_buses(cmd_bus):
    from hex.investigation.infra.repos import (
        DjangoCluesRepo, DjangoContactsForReviewRepo, DjangoBlacklistRepo,
    )
    from hex.investigation.infra.claude_agent import ClaudeCliAgent
    from hex.mailing.infra.repos import DjangoContactsRepo
    from hex.investigation.app import (
        ClassifyClue, ClassifyClueHandler,
        ExtractContact, ExtractContactHandler,
        ApproveContact, ApproveContactHandler,
        RejectContact, RejectContactHandler,
    )

    agent = ClaudeCliAgent()
    clues_repo = DjangoCluesRepo()
    cfr_repo = DjangoContactsForReviewRepo()
    bl_repo = DjangoBlacklistRepo()

    cmd_bus.subscribe(ClassifyClue, ClassifyClueHandler(clues_repo, cfr_repo, bl_repo, agent))
    cmd_bus.subscribe(ExtractContact, ExtractContactHandler(clues_repo, cfr_repo, bl_repo, agent))
    cmd_bus.subscribe(ApproveContact, ApproveContactHandler(cfr_repo, DjangoContactsRepo()))
    cmd_bus.subscribe(RejectContact, RejectContactHandler(cfr_repo, bl_repo))


i_bus = CommandBus()
