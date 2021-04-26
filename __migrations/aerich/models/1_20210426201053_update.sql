-- upgrade --
CREATE TABLE IF NOT EXISTS "____sub_module_fast_api_example_tortoise_orm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL
);
COMMENT ON TABLE "____sub_module_fast_api_example_tortoise_orm" IS 'Example model';
-- downgrade --
DROP TABLE IF EXISTS "____sub_module_fast_api_example_tortoise_orm";
