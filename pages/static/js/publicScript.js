
function findStory(n){
    var number = n;
    
    // ajax 로 스토리에 관련된 리뷰 내용만 보여주기
    $.ajax({
        url:'/Capstone/MovieGuide/getStory/',
        data:{'number':number},
        dataType:'json',
        success:function(args){
            var len = Object.keys(args).length;
            // alert(len);

            tc = 12;
            // var tc = len / 5;
            if(len % 5 != 0)
                tc = tc + 1;

            // 댓글 모음
            for(var i = 1; i <= len; i++){
                var t = args[i]['text'];
                var s = args[i]['senti'];

                // 해당 영화 리뷰 목록 접근
                var list = $('div#rNp_'+ number).find('table#myTable_' + number);
                var ele = '<tr><td><div class="reviewList_ele">';

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

                ele += '<span class="reviewText">' + skipText + '</span></div></td></tr>';
                
                list.append(ele);

                $('table.reviewTable').find('div.reviewList_ele').css('font-family', 'NanumSquareR');
                $('table.reviewTable').find('div.reviewList_ele').css('font-size', '1.7vw');
                $('table.reviewTable').find('div.reviewList_ele').css('color', 'rgb(221, 221, 221)');
                $('table.reviewTable').find('div.reviewList_ele').css('vertical-align', 'middle');

                $('table.reviewTable').find('img').css('width', '3%');
                $('table.reviewTable').find('img').css('height', 'auto');
                $('table.reviewTable').find('img').css('padding-bottom', '0.4%');
                $('table.reviewTable').find('img').css('height', 'auto');

                $('table.reviewTable').find('span').css('padding-left', '2%');
                $('table.reviewTable').find('span').css('cursor', 'auto');

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

function pageNavigator(){
    
}