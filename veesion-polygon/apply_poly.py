import argparse
import pickle
import numpy as np
from cv2 import fillPoly, imread, imwrite


def parser_create():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        "-i",
        help="input image path",
        required=True,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="output image path",
        default="caviar.jpeg"
    )
    parser.add_argument(
        "--original",
        "-c",
        help="original image on which polygons were calculated initially (for scaling)",
    )
    parser.add_argument(
        "--polygons",
        "-p",
        help="path to polygon file",
        required=True,
    )
    return parser


class Scaler:
    def __init__(self, x_scale: float = 1, y_scale: float = 1) -> None:
        self.sx = x_scale
        self.sy = y_scale

    @staticmethod
    def apply(x: int, y: int, sx: float, sy: float) -> [int, int]:
        #print(f"{x=} {y=} {sx=} {sy=}")
        return [int(x * sx), int(y * sy)]

    def __call__(self, x: int, y: int) -> [int, int]:
        return self.apply(x=x, y=y, sx=self.sx, sy=self.sy)

    @classmethod
    def from_absolute(cls) -> "Scaler":
        return Scaler(x_scale=1, y_scale=1)

    @classmethod
    def from_relative(cls, x_relative: float, y_relative: float) -> "Scaler":
        return Scaler(x_scale=x_relative, y_scale=y_relative)

    @classmethod
    def from_original(
        cls, x_original: int, y_original: int, x_dest: int, y_dest: int
    ) -> "Scaler":
        return Scaler(x_scale=x_dest / x_original, y_scale=y_dest / y_original)


def scale_polygons(polygons, original_res, target_res):
    if not polygons:
        return

    if original_res is None:
        scaler = Scaler.from_absolute()
    else:
        scaler = Scaler.from_original(
            x_original=original_res["width"],
            y_original=original_res["height"],
            x_dest=target_res[1],
            y_dest=target_res[0],
        )

    return [[scaler(x, y) for x, y in polygon] for polygon in polygons]


def main():
    parser_main = parser_create()
    try:
        config = parser_main.parse_args()
    except Exception as err:
        print(f"Error : {err}")
        return -1

    # Load input image
    image = imread(config.input)

    # Load polygons from file
    filehandler = open(config.polygons, 'rb')
    polygons = pickle.load(filehandler)

    # test new serialization:
    filehandler = open("testaz.obj", 'wb')
    pickle.dump({"shape":image.shape, "polygons": polygons}, filehandler)
    filehandler.close()
    filehandler = open("testaz.obj", 'rb')
    new_polygons = pickle.load(filehandler)
    polygons = new_polygons["polygons"]
    shape = new_polygons["shape"]

    print(f"loaded polygons: {shape}")
    print(polygons)

    # Apply scaling
    if config.original:
        image_original = imread(config.original)
        original_res = {"width":image_original.shape[1], "height":image_original.shape[0]}
        polygons = scale_polygons(polygons, original_res, image.shape)
        print("scaled polygons 1:")
        print(polygons)
        pouet = []
        for p in polygons:
            pnp = np.array(p, np.int32)
            pouet.append(pnp)
        print("scaled polygons 2:")
        print(pouet)
        polygons = pouet

    # Apply polygons
    fillPoly(image, polygons, 0)

    print(f"Saving {config.output}")
    imwrite(config.output, image)
    return 0


if __name__ == "__main__":
    main()
