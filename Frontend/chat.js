var $messages = $('.mCustomScrollbar'),
    d, h, m,
    i = 0;
var s = "00000000"+Math.floor(Math.random() * 100000)
var userId = s.substr(s.length-8, s.length);
var apigClient = apigClientFactory.newClient();
var params = {id:5,content:"what can i do for you?"};

$(window).on('load',function() {
  $messages.mCustomScrollbar({alwaysShowScrollbar: 2});
  setTimeout(function() {
	ResponseMessage("Hi there, I'm Sara, what can I help?");
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

$(document).on('click','#message-submit',function() {
	insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

function setDate(){
  d = new Date()
  console.log("in set date")
//  if (m != d.getMinutes()) {
    m = "0"+d.getMinutes();
    h = "0"+d.getHours();
    m = m.substr(m.length-2, m.length);
    h = h.substr(h.length-2, h.length);
    $('<div class="timestamp">' + h + ':' + m + '</div>').appendTo($('.message'));
//  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
  apigClient.messagePost({},{
	  id:userId,
	  content:msg
  },{})
  .then(function(result){
//	  console.log(result)
      body = result.data.body
      console.log(body)
      if(body != null){
	      var body_json = JSON.parse(body)
	      console.log(body_json.content)
	      ResponseMessage(body_json.content);
      }
      else{
    	  	  ResponseMessage("Sorry, I can't understand you, can you repeat?");
      }
    }).catch( function(result){
	      console.log(result)
    });
  
}
function ResponseMessage(msg) {
  $('<div class="message loading new"><figure class="avatar"><img src="./robot.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(function() {
    $('.message.loading').remove();
    $('<div class="message new"><figure class="avatar"><img src="./robot.png" /></figure>' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i++;
  }, 1000);

}