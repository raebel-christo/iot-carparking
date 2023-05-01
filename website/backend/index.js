const express = require('express');
const mongoose = require('mongoose');
const router = require('./routes')
const app = express();

app.use(express.json());
app.use(router);

mongoose
    .connect("mongodb+srv://raebelchristo:amber47@cluster0.c50zie8.mongodb.net/carparking?retryWrites=true&w=majority",{
    useNewUrlParser: true, useUnifiedTopology: true
})
    .then(()=>console.log("MongoDB connected pa"))
    .catch((err)=>console.log("Error", err));

app.listen(3000, ()=>{
    console.log("On port 3000");
});

const sleep = (ms)=>{
    return new Promise((resolve)=>setTimeout(resolve,ms)); 
}
const userModel = require('./models');

/*const main = async () => {
    await sleep(5000);
    
    const userModel = require('./models');

    const newUser = new userModel({
        // id: `ObjectId('644ea5da616332b2f98ce592')`,
        slot: "3",
        // plate: "TN04 GY3321",
        // in_time: `2023-04-30T17:31:05.734+00:00`,
    });

    newUser.save()
        .then(result=>console.log(result))
        .catch(err=>console.log(err));
};

main(); */
