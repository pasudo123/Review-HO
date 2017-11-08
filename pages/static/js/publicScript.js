
function findStory(n){
    var number = n;
    
    // ajax 로 스토리에 관련된 리뷰 내용만 보여주기
    $.ajax({
        url:'/Capstone/MovieGuide/getStory/',
        data:{'number':number},
        dataType:'json',
        success:function(args){
            var len = Object.keys(args).length;
            
            // 댓글 모음
            for(var i = 1; i <= len; i++){
                var t = args[i]['text'];
                var s = args[i]['senti'];

                // 해당 영화 리뷰 목록 접근
                var list = $('div#rNp_'+ number).find('div.reviewList');
                var ele = '<div class="reviewList_ele">';

                // 부정 리뷰
                if(s == 0){
                    ele += '<img class="reviewSenti" src="../static/Image/negIcon.png"></img>';
                }
                // 긍정 리뷰
                else{
                    ele += '<img class="reviewSenti" src="../static/Image/posIcon.png"></img>';
                }

                skipText = t;
                
                if(t.length >= 70)
                    skipText = t.substring(0, 70) + " ...";

                ele += '<span class="reviewText">' + skipText + '</span></div>';
                
                list.append(ele);

                // 다섯개씩 끊어서 목록 갱신
                if(i % 5 == 0)
                    break;
            }
        }
    });
}

function findSound(){
    // 음향에 관련된 리뷰들만 보여주기
}

function findAct(){
    // 연기에 관련된 리뷰들만 보여주기
}

function findSpelcial(){
    // 일단 보류 기능
}