/*

#---------------------------------------------------
# @author: DANDE TEJA         <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#---------------------------------------------------
*/


function build_model(){
  var annotation_text = document.getElementById('annotation_text').value;
 var doc = window.location.href.split("&image=")[1].split("&username=")[0]
  console.log('doc_name=',doc)
  document.getElementById('show_toast').click()
 document.getElementById('build_model_button').style.display = 'inline-block'
 var cnt=document.getElementById("progress_count2"); 
  var water=document.getElementById("water");
  var percent=0;
  var interval;
  var notification_red = true
  console.log('percentage: ',percent)
  interval=setInterval(function(){ 
    percent = percent + Math.floor(Math.random() * 10); 
    cnt.innerHTML = percent; 
    water.style.transform='translate(0'+','+(100-percent)+'%)';
    if(percent>=99){
      clearInterval(interval);
    }
  },2000);
 setTimeout(() => {
   console.log('timeout reached!')
   if(notification_red == true){
    show_notification_red()
    clearInterval(interval);
   } 
   return
 }, 60000);

  $.ajax({
        type: "POST",
        url: "/train?document="+doc,
        data: annotation_text,
        contentType: "text/xml",
        dataType: "text",
        success: function func(data)
        {
            console.log('inside train api ')
            response = data.split(",")
            document.getElementById('response_message').style.display = 'block'
              if(response[0] == "false")
              {
                  show_notification_red()
                  clearInterval(interval)
              }
              else {
                  console.log('model success!!!!!!!!!!!!')
                  notification_red = false             
                  show_notification_green()
                  percent = 100; 
                  cnt.innerHTML = percent; 
                  water.style.transform='translate(0'+','+(100-percent)+'%)';
                  clearInterval(interval)
                
              }
                 
              document.getElementById('build_model_button').style.display = 'none'
              return ;},
        error: function(xhr,ajaxOptions,thrownError) {
          console.log('Failed to execute train model')
          console.log(xhr.status);          
          console.log(thrownError);
        }
      });
}