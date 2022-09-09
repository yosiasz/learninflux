const sqlite3 = require('sqlite3').verbose()
const db = new sqlite3.Database('temps.db')

db.serialize(() => {
  db.run('DROP TABLE IF EXISTS Database')
  db.run('CREATE TABLE IF NOT EXISTS Database (data JSON)')
  const stmt = db.prepare('INSERT INTO Database (data) VALUES (?)')

  
  for (let i = 0; i < 100; i++) {
    let d = addHours(i); 
    let rand = getRandomFloat(i, 3.5, 2);    
    console.log(rand)
    // milliseconds since Jan 1, 1970, 00:00:00.000 GMT
    let ns = d.getTime();    
    stmt.run(`{"IP${i}" : [{"Electricity_reading": ${rand} ,"iso": "${d.toISOString()}","location": "Garage ${i}", "timestamp": ${ns}]}`)
  }

  stmt.finalize()

   db.each('SELECT data FROM Database', (err, row) => {
    console.log(`${row.data}`)
  })
})

function addHours(numOfHours, date = new Date()) {
  date.setTime(date.getTime() + numOfHours * 60 * 60 * 1000);

  return date;
}

function getRandomFloat(min, max, decimals) {
  const str = (Math.random() * (max - min) + min).toFixed(decimals);

  return parseFloat(str);
}

db.close()
