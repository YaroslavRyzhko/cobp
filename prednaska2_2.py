from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    tags: list[str] = field(default_factory=list)

    
    def add_tag(self, tag):
        self.tags.append(tag)

