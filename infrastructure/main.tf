terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

# Data source to fetch the current Azure tenant ID
data "azurerm_client_config" "current" {}

# Resource group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# Storage Account
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  tags = {
    environment = "staging"
  }
}

# Storage Container
resource "azurerm_storage_container" "storage_container" {
  name                  = "scraping-data"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

#TODO: Fix this
# resource "azurerm_key_vault" "key_vault" {
#   name                = "berlinbirds-vault"
#   location            = var.location
#   resource_group_name = azurerm_resource_group.rg.name
#   sku_name            = "standard"
#   tenant_id           = data.azurerm_client_config.current.tenant_id

#   soft_delete_retention_days = 7
#   purge_protection_enabled   = true
# }



# # PostgreSQL Server
# resource "azurerm_postgresql_server" "postgresql_server" {
#   name                = var.postgresql_server_name
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name

#   sku_name = "B_Gen5_1"  # Basic, 1 vCore
#   storage_mb = 5120      # 5GB
#   version    = "11"

#   administrator_login          = "postgresadmin"
#   administrator_login_password = "ComplexPassword!2345"

#   ssl_enforcement_enabled = true
# }

# # PostgreSQL Database
# resource "azurerm_postgresql_database" "postgresql_database" {
#   name                = var.postgresql_database_name
#   resource_group_name = azurerm_resource_group.rg.name
#   server_name         = azurerm_postgresql_server.postgresql_server.name
#   charset             = "UTF8"
#   collation           = "English_United States.1252"
# }
