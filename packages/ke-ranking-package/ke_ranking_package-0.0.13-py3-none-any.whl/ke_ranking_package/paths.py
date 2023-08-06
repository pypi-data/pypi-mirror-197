class Paths:
    root_data_dir: str = "/home/jupyter/mnt/s3/search-research/data"
    model_dir: str = "/home/jupyter/mnt/s3/search-research/models"

    @staticmethod
    def model_filepath(model_dir, filename):
        return f"{model_dir}/{filename}"

    @staticmethod
    def data_dir(root_data_dir, day):
        return f"{root_data_dir}/{day}"
