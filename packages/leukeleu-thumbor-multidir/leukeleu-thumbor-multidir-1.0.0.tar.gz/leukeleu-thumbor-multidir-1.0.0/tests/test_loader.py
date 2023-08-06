from os.path import abspath, dirname, join

from preggy import expect
from thumbor.config import Config
from thumbor.context import Context
from thumbor.loaders import LoaderResult
from tornado.testing import AsyncTestCase as TestCase
from tornado.testing import gen_test

from tc_multidir.loader import load

PRIMARY_IMAGES_PATH = abspath(join(dirname(__file__), "../fixtures/images/"))
SECONDARY_IMAGES_PATH = abspath(join(dirname(__file__), "../fixtures/more-images/"))


class FileLoaderTestCase(TestCase):
    def setUp(self):
        super().setUp()
        config = Config(
            TC_MULTIDIR_PATHS=[
                PRIMARY_IMAGES_PATH,
                SECONDARY_IMAGES_PATH,
            ]
        )
        self.ctx = Context(config=config)

    async def load_file(self, file_name):
        return await load(self.ctx, file_name)

    @gen_test
    async def test_should_load_file_in_primary_dir(self):
        result = await self.load_file("screenshot.png")
        expect(result).to_be_instance_of(LoaderResult)
        with open(join(PRIMARY_IMAGES_PATH, "screenshot.png"), "rb") as img:
            expect(result.buffer).to_equal(img.read())
        expect(result.successful).to_be_true()

    @gen_test
    async def test_should_load_file_in_secondary_dir(self):
        result = await self.load_file("image with spaces.png")
        expect(result).to_be_instance_of(LoaderResult)
        with open(join(SECONDARY_IMAGES_PATH, "image with spaces.png"), "rb") as img:
            expect(result.buffer).to_equal(img.read())
        expect(result.successful).to_be_true()

    @gen_test
    async def test_should_fail_when_non_existent_file(self):
        result = await self.load_file("image_NOT.jpg")
        expect(result).to_be_instance_of(LoaderResult)
        expect(result.buffer).to_equal(None)
        expect(result.successful).to_be_false()

    @gen_test
    async def test_should_fail_when_outside_root_path(self):
        result = await self.load_file("../__init__.py")
        expect(result).to_be_instance_of(LoaderResult)
        expect(result.buffer).to_equal(None)
        expect(result.successful).to_be_false()
