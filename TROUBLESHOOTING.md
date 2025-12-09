## Troubleshooting

### Integration Not Appearing

If the Jotty integration does not appear after installation:

1. Verify all files are in custom_components/jotty/
2. Check file permissions are correct
3. Restart Home Assistant completely
4. Check logs for errors: Settings > System > Logs

### Connection Issues

If you cannot connect to your Jotty server:

1. Verify the server URL is correct and accessible
2. Test the health endpoint: http://jotty:1122/api/health
3. Check your API key is valid
4. Ensure no firewall is blocking the connection
5. Verify Home Assistant can reach the server network

### No Notes or Lists Showing

If the integration connects but shows no data:

1. **CRITICAL**: Verify "Home Assistant" category exists in Jotty app
2. Create the category in both Notes AND Lists sections
3. Category name must be exactly "Home Assistant" (case sensitive)
4. Create a test note in this category from the Jotty app
5. Wait 5 minutes for sync or force refresh from demo-dashboard

### Helpers Missing

If scripts or dashboard fail:

1. Verify all helpers are created
2. Check entity IDs match exactly
3. Use Settings > Devices & Services > Helpers to verify
4. Recreate any missing helpers

### Automations Not Working

If dropdowns do not update:

1. Verify automations are enabled
2. Check automation traces for errors
3. Manually trigger: Developer Tools > Actions > script.jotty_refresh_dashboard_data
4. Review Home Assistant logs

- [Jotty: Notes and lists for Home Assistant Installation Guide](INSTALLATION.md)