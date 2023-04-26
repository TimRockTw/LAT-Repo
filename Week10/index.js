'use strict';
const express=require('express'),configGet=require('config');

const {TextAnalyticsClient, AzureKeyCredential}=require("@azure/ai-text-analytics");
//Azure text sentiment
const endpoint=configGet.get("ENDPOINT");
const apikey =configGet.get("TEXT_ANALYICS_API_KEY");
 const app =express(); 

const port = process.env.PORT||process.env.port||301;//process.env.PORT||process.env.port是遠端伺服器使用 ||這邊是本地

app.listen(port,()=>{
    console.log(`listening on ${port}`);//`'不一樣`在ESC下面
    MS_TextSentimentAnalysis()
    .catch((err) =>{
        console.error("Error:", err);
    });
});

async function MS_TextSentimentAnalysis(){
    console.log("[MS_TextSentimentAnalysis] in");
    const analyticsClient  =new TextAnalyticsClient(endpoint,new AzureKeyCredential(apikey));
    let documents=[];
    documents.push("沒事");
    const results=await analyticsClient.analyzeSentiment(documents);
    console.log("[results]",JSON.stringify(results));
}