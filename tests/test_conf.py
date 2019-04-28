import unittest
import os

from gstackutils.conf import Config
from gstackutils.conf import EnvString  # , SecretString, Config
from gstackutils.conf import ConfigMissingError  # , ValidationError
# from gstackutils import ImproperlyConfigured


class ConfTestCase(unittest.TestCase):
    def setUp(self):
        os.chdir("tests/fixtures")
        os.makedirs(".git", exist_ok=True)
        os.environ["GSTACK_CONFIG_MODULE"] = "gstack_conf"
        os.environ["GSTACK_ENV_FILE"] = ".env"
        os.environ["GSTACK_SECRET_FILE"] = ".secret.env"
        os.environ["GSTACK_SECRET_DIR"] = "secrets"
        os.environ["GSTACK_THEME"] = "simple"
        os.environ["GSTACK_PG_HBA_ORIG"] = "pg_hba.conf"
        os.environ["GSTACK_PG_CONF_ORIG"] = "postgresql.conf"

    def tearDown(self):
        if os.path.isfile(os.environ["GSTACK_ENV_FILE"]):
            os.remove(os.environ["GSTACK_ENV_FILE"])
        if os.path.isfile(os.environ["GSTACK_SECRET_FILE"]):
            os.remove(os.environ["GSTACK_SECRET_FILE"])
        if os.path.isdir(os.environ["GSTACK_SECRET_DIR"]):
            for f in os.listdir(os.environ["GSTACK_SECRET_DIR"]):
                os.remove(os.path.join(os.environ["GSTACK_SECRET_DIR"], f))
            os.rmdir(os.environ["GSTACK_SECRET_DIR"])
        del os.environ["GSTACK_ENV_FILE"]
        del os.environ["GSTACK_SECRET_FILE"]
        del os.environ["GSTACK_SECRET_DIR"]
        del os.environ["GSTACK_CONFIG_MODULE"]
        del os.environ["GSTACK_THEME"]
        del os.environ["GSTACK_PG_HBA_ORIG"]
        del os.environ["GSTACK_PG_CONF_ORIG"]
        os.chdir("/src")


class TestConf(ConfTestCase):
    def test_main_conf(self):
        conf = Config()
        self.assertTrue(conf.is_dev)

    def test_nonexistent(self):
        conffield = EnvString()
        conffield._setup_field(Config(), "X")
        with self.assertRaises(ConfigMissingError):
            conffield.get(root=True)

    def test_simple_set_get(self):
        conf = Config()
        conf.set("ANIMAL", "dog")
        # peek in the file
        with open(os.environ["GSTACK_ENV_FILE"], "r") as f:
            self.assertEqual(f.read(), "ANIMAL=dog\n")
        self.assertEqual(conf.get("ANIMAL"), "dog")

    def test_default_used(self):
        conf = Config()
        self.assertEqual(conf.get("ANIMAL"), "duck")

    def test_delete(self):
        conf = Config()
        conf.set("ANIMAL", "dog")
        self.assertEqual(conf.get("ANIMAL"), "dog")
        conf.set("ANIMAL", None)
        self.assertEqual(conf.get("ANIMAL"), "duck")

    def test_bool(self):
        conf = Config()
        conf.set("DANGEROUS", True)
        self.assertEqual(conf.get("DANGEROUS"), True)
        os.environ["DANGEROUS"] = "True"
        self.assertEqual(conf.get("DANGEROUS", root=False), True)

#     def test_validation(self):
#         conffield = EnvString(min_length=5, max_length=9)
#         conffield._setup_field(self.config, "X")
#         with self.assertRaises(ValidationError):
#             conffield.set("x")
#         with self.assertRaises(ValidationError):
#             conffield.set("1234567890")
#         with self.assertRaises(ValidationError):
#             conffield.set(0)
#
#
# class TestSecretString(CleanConfTestCase):
#     def test_prepare(self):
#         conffield = SecretString(services={"s": (1000,)})
#         conffield._setup_field(self.config, "X")
#         conffield.set("x")
#         conffield.prepare(service="s")
#         p = os.path.join(self.config.secret_dir, "X")
#         with open(p, "r") as f:
#             self.assertEqual(f.read(), "x")
#         stat = os.stat(p)
#         self.assertEqual(stat.st_uid, 1000)
#         self.assertEqual(stat.st_gid, 1000)
#
#
# class TestConfig(unittest.TestCase):
#     def setUp(self):
#         os.chdir("tests/fixtures")
#         os.makedirs(".git", exist_ok=True)
#
#     def tearDown(self):
#         if os.path.isdir(".git"):
#             os.rmdir(".git")
#         if os.path.isfile(".env"):
#             os.remove(".env")
#         if os.path.isfile(".secret.env"):
#             os.remove(".secret.env")
#         if os.path.isdir(".files"):
#             for f in os.listdir(".files"):
#                 os.remove(os.path.join(".files", f))
#             os.rmdir(".files")
#         os.chdir("../..")
#
#     def test_wrong_prod(self):
#         os.rmdir(".git")
#         with self.assertRaises(ImproperlyConfigured):
#             Config()
#
#     def test_init(self):
#         conf = Config(
#             config_module="gstack_conf",
#             env_file_path=".env",
#             secret_file_path=".secret.env",
#             root_mode=True
#         )
#         # print(conf.fields)
#         self.assertEqual(conf.env_file_path, ".env")
#
#     def test_prepare(self):
#         conf = Config(
#             config_module="gstack_conf",
#             env_file_path=".env",
#             secret_file_path=".secret.env",
#         )
#         conf.set("SAIS", "o", no_validate=True)
#         with self.assertRaises(ValidationError):
#             conf.prepare('test')
#
#         self.assertEqual(conf.get("ANIMAL"), "duck")
#
#         conf.set("SAIS", "something", no_validate=True)
#         conf.prepare("test")
#
#         conf = Config(
#             config_module="gstack_conf",
#             env_file_path=".env",
#             secret_file_path=".secret.env",
#             root_mode=False,
#         )
#         self.assertEqual(conf.get("SAIS"), "something")
