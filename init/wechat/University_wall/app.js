
App({
    globalData:{
        image_nine:0,
        qual:0,
        upimgmessage:{},
        userlogin:{},
        djangourl:'http://192.168.42.111:15050/',
        access_token:''

    },

  /**
   * 当小程序初始化完成时，会触发 onLaunch（全局只触发一次）
   */
  onLaunch: function () {
    var that = this
      this.globalData.djangourl='http://192.168.42.111:15050/'
    var login = wx.getStorageSync("userlogin")
    console.log('quan',login);
    if(login){
        this.globalData.userlogin = login
    }
    let SocketTask = wx.connectSocket({
      url: 'ws://192.168.42.111:15050/ws/1/',
      // header:{
      //   'content-type': 'application/json'
      // },
      // protocols: ['protocol1'],
      success:res=>{
        console.log(res);
      }

    })
    SocketTask.onOpen((result) => {
      console.log('onOpen： true')
      console.log('open',that.globalData.userlogin.student_number);
      if(that.globalData.userlogin.student_number == undefined){}
      else{
      let con={
        type:'open',
        stu:that.globalData.userlogin.student_number}
      SocketTask.send({
        data:JSON.stringify(con),
        success:res=>{
          console.log('succ',res);
        },
        fail:e=>{
          console.log('fail',e);
        }
  
      
      })
    }
    
    })
    SocketTask.onMessage((result) => {console.log('onMessage： true')})
    SocketTask.onError((e)=>{
      console.log(e);
    })


    
  },

  /**
   * 当小程序启动，或从后台进入前台显示，会触发 onShow
   */
  onShow: function (options) {
    
  },

  /**
   * 当小程序从前台进入后台，会触发 onHide
   */
  onHide: function () {
    
  },

  /**
   * 当小程序发生脚本错误，或者 api 调用失败时，会触发 onError 并带上错误信息
   */
  onError: function (msg) {
    
  }

})
