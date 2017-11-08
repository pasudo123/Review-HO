/**
 * jQuery PageNavigator v1.0.0
 *
 * Copyright (c) Seok Kyun. Choi. 최석균
 * GNU Lesser General Public License
 * http://www.gnu.org/licenses/lgpl.html
 *
 * registered date 2014-04-03
 * http://syaku.tistory.com
 */

(function($) {
  $.jaPageNavigator = {
      group : $('#page_group')    // 페이지태그 영역
    , start : '.start'            // 처음페이지 태그
    , startx : '.startx'          // 처음페이지 없을경우 숨김 태그
    , prev : '.prev'              // 이전페이지 태그
    , prevx : '.prevx'            // 이전페이지 없을경우 숨김 태그
    , pageaction : '.pageaction'  // 페이지 번호 노출 영역
    , now : '.now'                // 현재페이지번호 태그
    , num : '.num'                // 페이지번호 태그
    , div : '.div'                // 페이지번호 분리 태그
    , next : '.next'              // 다음페이지 태그
    , nextx : '.nextx'            // 다음페이지 없을경우 숨김 태그
    , end : '.end'                // 마지막페이지 태그
    , endx : '.endx'              // 마지막페이지 없을경우 숨김 태그
    , prevpage : '.prevpage'      // 이전 1 페이지 태그
    , prevpagex : '.prevpagex'    // 이전 1 페이지 없을경우 숨김 태그
    , nextpage : '.nextpage'      // 다음 1 페이지 태그
    , nextpagex : '.nextpagex'    // 다음 1 페이지 없을경우 숨김 태그
    , url : null                  // 기본적인 파라메터
    , page : null                 // 현재페이지번호
    , total_count : '0'           // 총 레코드수
    , page_link : 10              // 페이지링크번호 노출 수
    , page_row : 10               // 레코드 노출 수
    , name : 'page'               // 페이지 파라메터 명
    , autosort : false            // 페이지번호 자동정렬 (선택된 번호가 중간에 위치) (버그있음)
    , tag : null                  // 인위적으로 노출할 위치
  };

  $.fn.jaPageNavigator = function(options) {
    var p = $.extend($.jaPageNavigator,{group : this},options);

    if ($(p.group).text() == '') {
      return;
    }

    var start = $(p.start,p.group);
    var startx = $(p.startx,p.group);
    
    // 이전 페이지 이동 ( -page_link)
    var prev = $(p.prev,p.group);
    var prevx = $(p.prevx,p.group);
    var pageaction = $(p.pageaction,p.group);
    var now = $(p.now,p.group);
    var num = $(p.num,p.group);
    var div = $(p.div,p.group);

    // 다음 페이지 이동 ( +page_link)
    var next = $(p.next,p.group);
    var nextx = $(p.nextx,p.group);
    var end = $(p.end,p.group);
    var endx = $(p.endx,p.group);

    // 다음 페이지 이동 (-1)
    var prevpage = $(p.prevpage,p.group);
    var prevpagex = $(p.prevpagex,p.group);

    // 다음 페이지 이동 (+1)
    var nextpage = $(p.nextpage,p.group);
    var nextpagex = $(p.nextpagex,p.group);

    var url = p.url;
    var loc = document.location.pathname + document.location.search;

    if (url == null) {
      url = loc;
      var regx = new RegExp("(\\?|&){0,1}" + p.name + "\\=[0-9]+","g");
      if (typeof url == 'string') url = url.replace(regx,'');
    }
    if (url.indexOf('?') > -1) { url += '&'; } else { url += '?'; }

    // 현재 페이지 값이 없는 경우
    var page = (p.page == null) ? null : parseInt(p.page);
    if (page == null) {
      var regx_page = new RegExp("" + p.name + "\=([0-9]+)");
      regx_page.exec(loc);
      page = parseInt(RegExp.$1);
      if (page == '' || isNaN(page) ) page = 1;
    }

    var total_count = parseInt(p.total_count);
    var page_row = p.page_row;
    var page_link = p.page_link;
    var total_page = Math.floor((total_count - 1) / page_row) + 1;
    var start_page = Math.floor((page - 1) / page_link) * page_link + 1;
    var end_page = start_page + (page_link - 1);
    var now_page = Math.floor(start_page / page_link) + 1;
    var next_page = end_page + 1;
    var prev_page = start_page - 1;

    function search_alink(target) {
      if (jQuery('a',target).is('a')) {
        return 1;
      } else if (jQuery(target).is('a')) {
        return 2;
      } else {
        return 0;
      }
    }

    function alink(target,page_url,num,page) {
      if (parseInt(page) > 0) {
        var item = target.html();
        item = item.replace('{page}',page);
        item = item.replace('{page_link}',page);
        target.html(item);
      }

      if (p.tag != null) page_url += p.tag;

      if (num == 1) {
        jQuery('a',target).attr('href',page_url);
      } else if (num == 2) {
        jQuery(target).attr('href',page_url);
      } else {
      }

      return target;
    }

    if (!isNaN(total_page) && total_page > 0) {
      if (end_page > total_page ) { end_page = total_page; }

      var s,e;

      if (p.autosort) {
        var link = Math.floor(page_link/2);
        var n = page + link;
        s = page - link;
        e = n;
        if (0 >= s) { s = 1; }
        if (total_page <= n) { e = total_page; }
        prev_page = s;
        next_page = e;
      } else {
        s = start_page;
        e = end_page;
      }

      var num_link = search_alink(num);
      for (var i = s; i <= e; i++) {

      if (i == page) { 
        var h = jQuery(now).clone();
        var item = h.html();
        h.html(item.replace('{page}',i));
        pageaction.before(h);
      } else { 
        var h = jQuery(num).clone();
        pageaction.before(alink(h,url + p.name + '=' + i,num_link,i));
      }

        if (i != e) { pageaction.before(jQuery(div).clone()); }
      }

      pageaction.remove();
      now.remove();
      num.remove();
      div.remove();
      
      // 처음 페이지
      if (start.is(p.start)) {
      start.hide();
      startx.hide();
      if (page != 1) { 
        alert("처음 페이지" + prevpage + ", " + url + ", " + p.name + ", " + (page-1),search_alink(prevpage),(page-1));
        alink(start,url + p.name + '=1',search_alink(start),1);
        start.show();
      } else { startx.show(); }
      }

      // 이전 1 페이지
      if (prevpage.is(p.prevpage)) {
      prevpage.hide();
      prevpagex.hide();
      if(page > 1) { 
        alert("이전 1 페이지" + prevpage + ", " + url + ", " + p.name + ", " + (page-1),search_alink(prevpage),(page-1));
        alink(prevpage,url + p.name + '=' + (page-1),search_alink(prevpage),(page-1));
        prevpage.show();
      } else { prevpagex.show(); }
      }
      
      // 이전 페이지
      if (prev.is(p.prev)) {
      prev.hide();
      prevx.hide();
      if(now_page != 1 && total_page > 1) { 
        alert("이전 페이지" + prevpage + ", " + url + ", " + p.name + ", " + (page-1),search_alink(prevpage),(page-1));
        alink(prev,url + p.name + '=' + prev_page,search_alink(prev),prev_page);
        prev.show();
      } else { prevx.show(); }
      }
      
      // 다음 1 페이지
      if (nextpage.is(p.nextpage)) {
      nextpage.hide();
      nextpagex.hide();
      if (page < total_page) { 
        alert("다음 1 페이지" + prevpage + ", " + url + ", " + p.name + ", " + (page-1),search_alink(prevpage),(page-1));
        alink(nextpage,url + p.name + '=' + (page+1),search_alink(nextpage),(page+1));
        nextpage.show();
      } else { nextpagex.show(); }
      }
      
      // 다음 페이지
      if (next.is(p.next)) {
        next.hide();
        nextx.hide();
        if (end_page < total_page) {
          alert("다음페이지" + prevpage + ", " + url + ", " + p.name + ", " + (page-1),search_alink(prevpage),(page-1)); 
          alink(next,url + p.name + '=' + next_page,search_alink(next),next_page);
          next.show(); 
        } else { nextx.show(); }
      }
      
      // 마지막 페이지
      if (end.is(p.end)) {
        end.hide();
        endx.hide();
        if (page != total_page) { 
          alert("마지막 페이지" + prevpage + ", " + url + ", " + p.name + ", " + (page-1),search_alink(prevpage),(page-1));
          alink(end,url + p.name + '=' + total_page,search_alink(end),total_page);
          end.show();
        } else { endx.show(); }
      }

      // 토탈 페이지수가 링크수보다 적기때문에 처음과 마지막 페이지 필요없음
      if (page_link > total_page) {
        start.remove();
        end.remove();
      }
      this.show();
    } else {
      this.hide();
    }

    return this;
  };

})(jQuery);