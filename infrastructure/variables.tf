variable "location" {
  description = "Azure region to host all resources"
  default     = "westeurope"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group to be created."
  default     = "berlinbirds"
  type        = string
}

variable "storage_account_name" {
  default = "berlinbirdsstorage713"
  type    = string
}

variable "postgresql_server_name" {
  default = "berlinbirds-PostgresSQLServer"
  type    = string
}

variable "postgresql_database_name" {
  default = "berlinbirds-staging-database"
  type        = string
}
