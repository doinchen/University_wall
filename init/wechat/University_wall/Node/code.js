// const request = require('request')
var app = getApp();
const AK = "GUQ1GDI8a6p3Epwgr1IhyLzI"
const SK = "77Gt9l9npw5cIme5e4Kcx0EzQ198gGrE"
const tank = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='

const sendimg=(past,type,Token)=> { 
    return new Promise(function(resolve,reject){
         let base64 = getFileContentAsBase64(past)
         wx.request({
            url: 'https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined?access_token=' + Token,
            header: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            dataType:'json',
            method: 'POST',
            data: {
                'image':base64,
                'imgType':type
            },
            success:res=>{
                // console.log('code',res);
                app.globalData.up_img_message=res
                resolve(res);
            }
    })
    })

}

/**
 * 使用 AK，SK 生成鉴权签名（Access Token）
 * @return string 鉴权签名信息（Access Token）
 */

const getAccessToken=()  => {
    return new Promise(function(resolve,reject){
        wx.request({
        url: 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + AK + '&client_secret=' + SK,
        method: 'POST',
        success:res=>{

          app.globalData.access_token = res.data.access_token
          resolve(res.data)
        }
      })
    })

    //   console.log(app.globalData.access_token);
      return app.globalData.access_token
}

/**
 * 获取文件base64编码
 * @param string  path 文件路径
 * @return string base64编码信息，不带文件头
 */
function getFileContentAsBase64(path) {
    let aaaa = wx.getFileSystemManager().readFileSync(path, 'base64' );

    return aaaa;

}


function formatDate() {
  var date = new Date();
  var year = date.getFullYear();
  var month = date.getMonth() + 1;
  var day = date.getDate();
  var hh = date.getHours();
  var mm = date.getMinutes();
  var ss = date.getSeconds();
  var arr = ['日', '一', '二', '三', '四', '五', '六'];
  var week = arr[date.getDay()];

  function add0(val) {
      return (val < 10 ? '0' + val : val);
  }
  month = add0(month);
  day = add0(day);
  hh = add0(hh);
  mm = add0(mm);
  ss = add0(ss);
  return year + '-' + month + '-' + day + ' ' + hh + ':' + mm + ':' + ss

}


module.exports = {
    getAccessToken:getAccessToken,
    getFileContentAsBase64:getFileContentAsBase64,
    formatDate:formatDate,

    sendimg:sendimg,
    tank:tank,
    AK:AK,
    SK:SK

}