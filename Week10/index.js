'use strict';
const   line=require('@line/bot-sdk'),
       express=require('express'),
        configGet=require('config');

const {TextAnalyticsClient, AzureKeyCredential}=require("@azure/ai-text-analytics");

//line config
const configLine = {
    channelAccessToken:configGet.get("CHANNEL_ACCESS_TOKEN"),
    channelSecret:configGet.get("CHANNEL_SECRET")
  };

//Azure text sentiment
const endpoint=configGet.get("ENDPOINT");
const apikey =configGet.get("TEXT_ANALYICS_API_KEY");
const client = new line.Client(configLine);
const app =express(); 

const port = process.env.PORT||process.env.port||3001;//process.env.PORT||process.env.port是遠端伺服器使用 ||這邊是本地

app.listen(port,()=>{
    console.log(`listening on ${port}`);//`'不一樣`在ESC下
});

async function MS_TextSentimentAnalysis(thisEvent){
    console.log("[MS_TextSentimentAnalysis] in");
    const analyticsClient  =new TextAnalyticsClient(endpoint,new AzureKeyCredential(apikey));
    let documents=[];
    documents.push(thisEvent.message.text);
    const results=await analyticsClient.analyzeSentiment(documents);
    console.log("[results]",JSON.stringify(results));

    const echo = {
        type: 'text',
        text: results[0].sentiment
      };
      return client.replyMessage(thisEvent.replyToken, echo);
}

app.post('/callback', line.middleware(configLine),(req, res)=>{
  Promise
    .all(req.body.events.map(handleEvent))
    .then((result)=>res.json(result))
    .catch((err)=>{
      console.error(err);
      res.status(500).end();
    });
});

function handleEvent(event){
    if(event.type !== 'message' || event.message.type !== 'text'){
      return Promise.resolve(null);
    }
  
    MS_TextSentimentAnalysis(event)
      .catch((err) => {
        console.error("Error:", err);
      }); 
  }