let animation = null
let viewHeight = 0
const app = getApp()

Page({
  data: {
      aaa:false,
    videoList: [
        {
            "id": "33",
            "user": {
                "username": "杜宇琛",
                "avatarurl": "http://192.168.42.111:15050/media/user/asdfas20230209004933.jpg"
            },
            "campus": "鹿泉校区",
            "department": "信息技术与文化管理学院",
            "profession": "网络工程",
            "create_time": {
                "time01": "5分钟前",
                "time02": "2023-02-09T17:06:34",
                "time03": "20230209170634"
            },
            "admin_hide": "True",
            "user_hide": "True",
            "type": "video",
            "text": "sfsfasdfsa",
            "type_text": {
                "video_url": "http://192.168.42.111:15050/media/taskimg/20230209170634210809039040.mp4",
                "video_image": "http://192.168.42.111:15050/media/taskimg/20230209170634210809039040.jpg"
            },
            "favor_count": 0,
            "viewer_count": 0,
            "comment_count": 0,
            "time_TS": "20230209170634"
        },{
            "id": "34",
            "user": {
                "username": "杜宇琛",
                "avatarurl": "http://192.168.42.111:15050/media/user/asdfas20230209004933.jpg"
            },
            "campus": "鹿泉校区",
            "department": "信息技术与文化管理学院",
            "profession": "网络工程",
            "create_time": {
                "time01": "5分钟前",
                "time02": "2023-02-09T17:06:34",
                "time03": "20230209170634"
            },
            "admin_hide": "True",
            "user_hide": "True",
            "type": "video",
            "text": "sfsfasdfsa",
            "type_text": {
                "video_url": "http://192.168.42.111:15050/media/taskimg/20230209170634210809039040.mp4",
                "video_image": "http://192.168.42.111:15050/media/taskimg/20230209170634210809039040.jpg"
            },
            "favor_count": 0,
            "viewer_count": 0,
            "comment_count": 0,
            "time_TS": "20230209170634"
        },{
            "id": "11",
            "user": {
                "username": "杜宇琛",
                "avatarurl": "http://192.168.42.111:15050/media/user/asdfas20230209004933.jpg"
            },
            "campus": "鹿泉校区",
            "department": "信息技术与文化管理学院",
            "profession": "网络工程",
            "create_time": {
                "time01": "5分钟前",
                "time02": "2023-02-09T17:06:34",
                "time03": "20230209170634"
            },
            "admin_hide": "True",
            "user_hide": "True",
            "type": "video",
            "text": "sfsfasdfsa",
            "type_text": {
                "video_url": "http://192.168.42.111:15050/media/taskimg/20230209170634210809039040.mp4",
                "video_image": "http://192.168.42.111:15050/media/taskimg/20230209170634210809039040.jpg"
            },
            "favor_count": 0,
            "viewer_count": 0,
            "comment_count": 0,
            "time_TS": "20230209170634"
        },
     
    ],
    oldId: -1,
    startPage: 0,
    animationData: {},
    viewIndex: 0
  },
  onLoad: function () {
    this.getViewHeight()
    this.getVideoCtx(0)
  },
  getVideoCtx(id) {
    // 有上一个
    if(this.data.oldId > -1) {
      wx.createVideoContext(`video-${this.data.oldId}`).pause()
    }
    const ctx = wx.createVideoContext(`video-${id}`)
    // console.log(ctx)
    ctx.play()
    this.setData({
      oldId: id
    })
  },
  // 触摸开始
  onTouchStart({ touches }) {
    const { pageY } = touches[0]
    this.setData({
      startPage: pageY
    })
    // console.log('按下',pageY)
  },
  // 触摸移动
  onTouchMove({ touches }) {
    // const { pageY } = touches[0]
    // console.log('移动',pageY)
  },
  // 触摸结束
  onTouchEnd({ changedTouches }) {
    const { pageY } = changedTouches[0]
    const diff = pageY - this.data.startPage
  
    if(Math.abs(diff) <= 30) {
      console.log('不触发')
      return
    }
  
    if(diff > 0) {
      this.setAni(1)
    }else if( diff == 0) {
      this.setAni(0)
    }else{
      this.setAni(-1)
    }
  },
  // 滑动动画 0 不移动 -1 上拉 1 下拉
  async setAni(status) {
    if(status == 0) return false
    
    if(!animation) {
      animation = wx.createAnimation({
        duration: 500,
        timingFunction: 'ease'
      });
    }
    if(!viewHeight) {
      await this.getViewHeight()
    }
    // 计算位移
    let moveY = 0
    let nowIndex = this.data.viewIndex
    status > 0 ? nowIndex-- : nowIndex++
    if(nowIndex < 0) {
      wx.showToast({
        title: '到顶部了'
      })
      return
    }
    if(nowIndex == this.data.videoList.length) {
      wx.showToast({
        title: '到底了哦'
      })
      return
    }
    moveY = -1 * nowIndex * viewHeight
    animation.translateY(moveY).step()
    this.getVideoCtx(nowIndex)
    this.setData({
      animationData: animation.export(),
      viewIndex: nowIndex
    })
  },
  // 获取dom高度
  getViewHeight() {
    return new Promise((resolve) => {
      const query = wx.createSelectorQuery()
      query.select(".item-1").boundingClientRect()
      query.exec(function (res) {
        if(res.length && res[0]) {
          viewHeight = res[0].height
          resolve(viewHeight)
        }
      })
    })
  },
  onLoad: function (options) {
    wx.request({
        url: app.globalData.djangourl+'api/WX_video_ground/',
        method:'GET',
        success:res=>{
            console.log(res);
            this.setData(
                {
                    videoList:res.data
                }
            )
        }
      })

      
    
  },
  onShow: function () {
    wx.request({
      url: app.globalData.djangourl+'api/WX_video_ground/',
      method:'GET',
      success:res=>{
          console.log(res);
          this.setData(
              {
                videoList:res.data
              }
          )
      }
    })
  
},
})