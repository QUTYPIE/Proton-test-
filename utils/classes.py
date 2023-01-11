from dataclasses import dataclass, field



@dataclass
class Profile:
    """User profile class for EpicBot's profile system."""

    # basic stuff
    _id: int
    badges: list = field(default_factory=lambda: ["normie"])
