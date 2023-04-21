# Start database and verify connection
echo "Starting mongod daemon...";
sudo systemctl start mongod;
sudo systemctl status mongod;

# Delete and Insert documents
node create-entries.js;

