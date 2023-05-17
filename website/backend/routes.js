const express = require('express');
const userModel = require('./models');
const app = express();

app.post("/add_user", async (request, response) => {
    console.log("entering post");
    const user = new userModel(request.body);

    try {
      console.log("awaiting save");
      await user.save();
      console.log("save done");
      response.send("done");
    } catch (error) {
      response.status(500).send(error);
    }
});

app.get("/users", async (request, response) => {
    const users = await userModel.find();
    try {
      response.send(users);
    } catch (error) {
      response.status(500).send(error);
    }
});

module.exports = app;

