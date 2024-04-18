output "storage_account_primary_connection_string" {
  value     = azurerm_storage_account.storage.primary_connection_string
  sensitive = true
}

# output "postgresql_server_fqdn" {
#   value = azurerm_postgresql_server.postgresql_server.fqdn
# }
