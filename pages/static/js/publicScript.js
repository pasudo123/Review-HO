
function findStory(n){
    var number = n;
    
    // ajax 로 스토리에 관련된 리뷰 내용만 보여주기
    $.ajax({
        url:'/Capstone/MovieGuide/getStory/',
        data:{'number':number},
        dataType:'json',
        success:function(args){
            
            $('table.reviewTable').find('tr').remove();
            $('div.pagination').find('ul').remove();

            var len = Object.keys(args).length;

            pageSize = len / 5;
            // 나머지 확인
            if(len % 5 != 0)
                pageSize += 1; 

            var textArr = new Array();
            var sentArr = new Array();

            // 댓글 모음
            for(var i = 1; i <= len; i++){
                var t = args[i]['text'];
                var s = args[i]['senti'];
                
                textArr[i] = t;
                sentArr[i] = s;

                // +++++++++++++++처음 다섯개만
                if(i <= 5){
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
                    
                    if(t.length >= 65)
                        skipText = t.substring(0, 65) + " ...";

                    ele += '<span class="reviewText"><a class="hastip" title=\'' + t + '\'>' + skipText + '</a></span></div></td></tr>';
                    
                    list.append(ele);

                    $('table.reviewTable').find('td').css('padding-top', '0.7%');
                    $('table.reviewTable').find('td').css('padding-bottom', '0.7%');

                    $('table.reviewTable').find('div.reviewList_ele').css('font-family', 'NanumSquareR');
                    $('table.reviewTable').find('div.reviewList_ele').css('font-size', '1.7vw');
                    $('table.reviewTable').find('div.reviewList_ele').css('color', 'rgb(221, 221, 221)');
                    $('table.reviewTable').find('div.reviewList_ele').css('vertical-align', 'middle');

                    $('table.reviewTable').find('img').css('width', '3%');
                    $('table.reviewTable').find('img').css('height', 'auto');

                    $('table.reviewTable').find('span').css('padding-left', '2%');
                    $('table.reviewTable').find('span').css('cursor', 'default');

                    $('table.reviewTable').find('span').find('a').css('color', 'white');
                    $('table.reviewTable').find('span').find('a').hover(function(){
                        $(this).css('color','#a7cdc6');
                        $(this).css('text-decoration', 'none');
                        },
                        function(){ $(this).css('color','white');
                    });

                    // $('table#myTable_' + number).find('a').tooltipsy({
                    //     className: 'myTooltip',
                    //     offset: [0, 10],
                    //     show: function (e, $el) {
                    //         $el.fadeIn(100);
                    //     },
                    //     hide: function (e, $el) {
                    //         $el.fadeOut(500);
                    //     }
                    // });
                }
                // +++++++++++++++처음 다섯개만
            }

            $('#pagination_'+number).materializePagination({
                align: 'center',
                lastPage: pageSize,
                firstPage: 1,
                useUrlParameter: false,
                onClickCallback: function(requestedPage) {
                    // 해당 페이지 넘버 반환
                    // alert(requestedPage);
                    startP = (requestedPage - 1) * 5 + 1;
                    endP = requestedPage * 5;

                    $('table.reviewTable').find('tr').remove();

                    // 해당 페이지에 맞는 리뷰반환
                    for(var i = startP; i <= endP; i++){
                        var t = textArr[i];
                        var s = sentArr[i];

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
                        
                        if(skipText == null)
                            break;
                        if(t.length >= 65)
                            skipText = t.substring(0, 65) + " ...";

                        ele += '<span class="reviewText"><a title=\'' + t + '\'>' + skipText + '</a></span></div></td></tr>';
                        
                        list.append(ele);

                        $('table.reviewTable').find('td').css('padding-top', '0.7%');
                        $('table.reviewTable').find('td').css('padding-bottom', '0.7%');

                        $('table.reviewTable').find('div.reviewList_ele').css('font-family', 'NanumSquareR');
                        $('table.reviewTable').find('div.reviewList_ele').css('font-size', '1.7vw');
                        $('table.reviewTable').find('div.reviewList_ele').css('color', 'rgb(221, 221, 221)');
                        $('table.reviewTable').find('div.reviewList_ele').css('vertical-align', 'middle');

                        $('table.reviewTable').find('img').css('width', '3%');
                        $('table.reviewTable').find('img').css('height', 'auto');

                        $('table.reviewTable').find('span').css('padding-left', '2%');
                        $('table.reviewTable').find('span').css('cursor', 'default');

                        $('table.reviewTable').find('span').find('a').css('color', 'white');
                        $('table.reviewTable').find('span').find('a').hover(function(){
                            $(this).css('color','#a7cdc6');
                            $(this).css('text-decoration', 'none');
                            },
                            function(){ $(this).css('color','white');
                        });

                        // $('table#myTable_' + number).find('a').tooltipsy({
                        //     className: 'myTooltip',
                        //     offset: [0, 10],
                        //     show: function (e, $el) {
                        //         $el.fadeIn(100);
                        //     },
                        //     hide: function (e, $el) {
                        //         $el.fadeOut(500);
                        //     }
                        // });
                    }

                    console.log('Requested page from #pagination : ' + requestedPage);
                }
            });

            // 부트스트랩 css 조정
            $('#pagination_' + number).find('ul').css('margin', '0');
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

