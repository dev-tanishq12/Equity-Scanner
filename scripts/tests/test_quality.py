from scripts.processing.quality import DataQuality


def main():

    quality = DataQuality()

    quality.validate()


if __name__ == "__main__":
    main()