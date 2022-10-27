data "terraform_remote_state" "ecr" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/dev_kpi_calculation_platform/ecr.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "s3" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/dev_kpi_calculation_platform/s3.tfstate"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "glue_database" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/shared/dev_kpi_calculation_platform/glue/database.tfstate"
    region = "us-east-1"
  }
}


data "terraform_remote_state" "glue_tables" {
  backend = "s3"
  config = {
    bucket = "waste-labs-terraform-backends"
    key    = "env:/${terraform.workspace}/dev_kpi_calculation_platform/glue/tables.tfstate"
    region = "us-east-1"
  }
}
