from pydantic import BaseSettings


class GeneweaverTestingConfig(BaseSettings):
    """The pydantic configuration class definition for the geneweaver.testing package."""

    LOG_LEVEL: str = 'DEBUG'

    class Config:
        """The config class for pydantic object.

        Used here to configure the default means of determining settings for the package.
        """

        env_prefix = 'GENEWEAVER_TESTING_'
        case_sensitive = True
        env_file = ".env"