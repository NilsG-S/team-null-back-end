var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var appointments = require('./appointments');
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


app.get('/', function (req, res) {
  res.send('Hello World!')
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
});



app.use('/appointments', appointments);


// app.post('/appointments', (req, res) => {
//   var body = req.body;
//   var params = {
//     employee_id     :body.employee_id,
//     patient_id      :body.patient_id,
//     date_time       : new Date(body.date_time),
//     completed       :0
//   };
//   var query = connection.query("INSERT INTO APPOINTMENTS SET ?",
//                                 params, (err, response, fields) => {
//                                   if (err) throw err;
//                                   console.log(response.insertId);
//                                 });
// });
