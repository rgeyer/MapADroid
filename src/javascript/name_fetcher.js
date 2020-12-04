
const uri = process.env.URI
const token = process.env.API_TOKEN

const dbConfig = {
  'host': process.env.DB_HOST,
  'user': process.env.DB_USER,
  'password': process.env.DB_PASS,
  'database': process.env.DB_NAME,
  'port': process.env.DB_PORT ? process.env.DB_PORT : '3306',
}

// don't edit anything below this line
try {
  console.log('Starting namefetcher')

  const axios = require('axios')
  const mysql = require('mysql2')
  const db = mysql.createConnection(dbConfig)
  const settings = {
    gym: { table: 'gymdetails', imageCol: 'url', id: 'gym_id', type: 'gyms' },
    stop: { table: 'pokestop', imageCol: 'image', id: 'pokestop_id', type: 'stops' }
  }

  async function dbUpdate(data, settings) {
    for (detail of data) {
      console.log(` --> Updating ${detail.id}: ${detail.name}`)

      if (detail.imageUrl == null || detail.imageUrl === '?') {
        await db.promise().execute(`UPDATE ${settings.table} set name=? WHERE ${settings.id}=?`, [detail.name, detail.id])
      } else {
        await db.promise().execute(`UPDATE ${settings.table} set name=?, ${settings.imageCol}=? WHERE ${settings.id}=?`, [detail.name, detail.imageUrl, detail.id])
      }
    }
  }

  async function askApiAndUpdate(req, settings) {
    let count = 0

    for(i=0, j=req.length, c=50; i < j; i += c) {
      const payload = Array.from(req.slice(i, i + c), r => r.id)

      console.log(`Chunk ${i/c+1}/${Math.ceil(req.length/c)} (${payload.length} ${settings.type})`)

      await axios.post(`${uri}${token}`, payload)
        .then(async response => {
          count += response.data.length
          await dbUpdate(response.data, settings)
        })
    }

    return count
  }

  (async () => {
    for (x of Object.keys(settings)) {
      await db.promise().query(`SELECT ${settings[x].id} as id FROM ${settings[x].table} WHERE (name IS NULL OR name="unknown") AND LENGTH(${settings[x].id}) > 32`)
        .then(async ([dbret]) => {
          console.log(`\nRequesting ${dbret.length} unknown ${x.type} from API`)
          const count = await askApiAndUpdate(dbret, settings[x])
          console.log(`API returned ${count} ${x} names`)
        })
    }
  })().then(() => {
    console.log("\nBye!")
    db.end()
    process.exit(0)
  }).catch(e => {
    console.log("YOU EITHER FORGOT TO PROVIDE AN API KEY OR THE API IS PROBABLY DOWN AND YOU JUST GOTTA WAIT A BIT!")
    db.end()
    process.exit(1)
  })
} catch(e) {
  if (e instanceof Error && e.code === 'MODULE_NOT_FOUND') {
    console.log('Cannot load requirements! please run `npm i mysql2 axios` first!')
    process.exit(1)
  } else {
    console.log(e)
  }
}
