provider "aws" {
  region = var.region
}


locals {
  env = terraform.workspace

  database = data.terraform_remote_state.database.outputs.database
  tables = {
    "kpi"   = "${local.env}_kpi"
    "stops" = "${local.env}_stops"
  }
  s3_bucket_name = data.terraform_remote_state.s3.outputs.s3_bucket_id
  tags = {
    region = var.region
    name   = var.project_name
    env    = terraform.workspace
  }
}


resource "aws_glue_catalog_table" "kpi" {
  name          = local.tables["kpi"]
  database_name = local.database

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${local.s3_bucket_name}/${local.env}/02_primary/kpi/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = local.tables["kpi"]
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name    = "filename"
      type    = "string"
      comment = "Filename record extracted from."
    }

    columns {
      name    = "process_datetime"
      type    = "timestamp"
      comment = "Processing timestamp."
    }

    columns {
      name    = "travel_path"
      type    = "string"
      comment = "LINESTRING of travel path over the stops."
    }

    columns {
      name    = "distance_km"
      type    = "double"
      comment = "Overall route travel distance."
    }

    columns {
      name    = "duration_hour"
      type    = "double"
      comment = "Overall route travel duration."
    }

  }
  partition_keys {
    name    = "processing_id"
    type    = "string"
    comment = "File primary key with format YYYY-MM-DD HH:MI:SS__FILENAME"
  }

}


resource "aws_glue_partition_index" "kpi_parition_index" {
  database_name = local.database
  table_name    = aws_glue_catalog_table.kpi.name

  partition_index {
    index_name = "${local.tables["kpi"]}_partition_index"
    keys       = ["processing_id"]
  }
}


resource "aws_glue_catalog_table" "stops" {
  name          = local.tables["stops"]
  database_name = local.database

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${local.s3_bucket_name}/${local.env}/02_primary/stops/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = local.tables["stops"]
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name    = "latitude"
      type    = "double"
      comment = "Coordinates latitude."
    }

    columns {
      name    = "longitude"
      type    = "double"
      comment = "Coordinates longitude."
    }

    columns {
      name    = "stop_id"
      type    = "string"
      comment = "Stop unique identifier."
    }

    columns {
      name    = "route_sequence"
      type    = "int"
      comment = "Sequence number according stop must be visited."
    }

    columns {
      name    = "filename"
      type    = "string"
      comment = "Filename record extracted from."
    }

    columns {
      name    = "process_datetime"
      type    = "timestamp"
      comment = "Processing timestamp."
    }

    columns {
      name    = "dur_from_prev_point_hour"
      type    = "double"
      comment = "Travel duration (hours) is needed to reach current point from previous."
    }

    columns {
      name    = "dist_from_prev_point_km"
      type    = "double"
      comment = "Travel distance (kilometers) is needed to reach current point from previous."
    }

  }
  partition_keys {
    name    = "processing_id"
    type    = "string"
    comment = "File primary key with format YYYY-MM-DD HH:MI:SS__FILENAME"
  }

}


resource "aws_glue_partition_index" "stops_parition_index" {
  database_name = local.database
  table_name    = aws_glue_catalog_table.stops.name

  partition_index {
    index_name = "${local.tables["stops"]}_partition_index"
    keys       = ["processing_id"]
  }
}
