$(document).ready(function () {

	$('#btn-login').bind('click', function() {
		$('#loginPopup').attr('style', 'display: block;');
	});

	$('#btn-close').bind('click', function() {
		$('#loginPopup').attr('style', 'display: none;');
	});
	
	$('#slip-banner-wrapper').bind('click', function() {
		$('#baseModal').append(`<div class="modal-content modal-overlay sell-bet-help-modal">
	   <div class="sell-bet-help-modal animate inner-slide-content">
	      <div class="title">
	         <div class="titleC"> <i class="icon-bet-sell"></i> <span>Продажа ставки</span> </div>
	      </div>
	      <div class="desc1">
	         <div class="desc1C">Для продажи ставки, Вам нужно открыть купон с неразыгранными ставками и выбрать ставку, которую Вы хотели бы продать.</div>
	      </div>
	      <h1 class="title">Неразыгранные ставки</h1>
	      <div class="unplayed-bets">
	         <span>Динамо Киев - Челси Лондон</span> 
	         <ul class="fakeBet">
	            <div class="right "> <span>12.8<i>@</i>50.00</span> <i class="icon-bet-sell"></i> </div>
	            <div class="slipBets ">
	               <div class="betType">1X2&nbsp;-&nbsp;</div>
	               <div class="betChoice">1</div>
	            </div>
	         </ul>
	      </div>
	      <div class="bet-desc"> В деталях ставки найдите пункт <b>"Продажа ставки"</b> и нажмите кнопку <b class="uppercase">"ПРОДАТЬ"</b>  </div>
	      <ul id="detailsList" class="list">
	         <li>
	            <span>Сумма ставки:</span> <span>50.00 RUB</span>
	            <hr>
	         </li>
	         <li id="cashoutBlock">
	            <span>Продажа ставки:</span> <span id="cashoutAmount"> 45.00 RUB <a id="cashoutBtn" class="button">Продать</a> </span> 
	            <hr>
	         </li>
	      </ul>
	   </div>
	</div>
	<div class="modal-nav">  <div class="close"> <div class="ico-holder"></div> </div>   </div>`);
		$('.close').bind('click', function() {
			$('.modal-content').remove();
			$('.close').remove();
		});
	});

});