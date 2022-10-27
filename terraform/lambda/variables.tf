variable "region" {
  type        = string
  description = "Project deployment region"
}

variable "project_name" {
  type        = string
  description = "Project name"
}


variable "build_tag" {
  type        = string
  default     = "5"
  description = "Project name"
}
