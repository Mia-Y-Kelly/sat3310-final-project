const { MongoClient } = require("mongodb");

// Replace the following with values for your environment.
const username = encodeURIComponent("usernam-here");
const password = encodeURIComponent("password-here");
const url = "ip-address";
const defaultdb = "admin"

// Replace the following with your MongoDB deployment's connection string.
const uri =
  `mongodb://${username}:${password}@${url}/?authSource=${defaultdb}`;

// Create a new MongoClient
const client = new MongoClient(uri);

// Function to connect to the server
async function run() {
  try {
    // Establish and verify connection
    await client.connect();
    console.log("Connected successfully to server");

    // const db = client.db('classdb');
    const db = client.db('classdb');
    const col = db.collection('Student');

    // Delete all existing documents
    const deleteAll = await col.deleteMany({});
    console.log(`Deleted ${deleteAll.deletedCount} documents`);

    // Insert new documents
    const result = await col.insertMany([
      {
        name: 'Alice',
        year: 'Sophomore'
      },
      {
        name: 'Bob',
        year: 'Freshman'
      },
      {
        name: 'Eve',
        year: 'Senior'
      }
    ]);

    console.log(`Inserted ${result.insertedCount} documents`);   
  } catch(err) {
    console.error(err);  
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}

run().catch(console.err);

