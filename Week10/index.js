'use strict';
const express=require('expess'),configGet=require('config');

const app =express(); //express 很強

const port = process.env.PORT||process.env.port||3001;//process.env.PORT||process.env.port是遠端伺服器使用 ||這邊是本地

app.listen(port,()=>{
    console.log(`listening on ${port}`);//`'不一樣`在ESC下面
});
