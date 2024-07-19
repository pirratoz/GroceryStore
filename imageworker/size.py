from dataclasses import dataclass


@dataclass
class Size:
    width: int
    height: int

    def get_tuple(self) -> tuple[int, int]:
        return (self.width, self.height)


@dataclass
class SizeImageS3(Size):
    path: str

    def get_size(self) -> Size:
        return Size(
            width=self.width,
            height=self.height,
        )
