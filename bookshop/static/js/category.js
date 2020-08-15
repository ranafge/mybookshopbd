var cardSpaces=15;
var middleDistance = 200;

	var nxtVal=middleDistance ;
	middleDistance-=cardSpaces;
	$(".next").each(function(){
		$(this).attr("elad-translate",nxtVal);
		$(this).css("transform","translateX(calc(-50% + "+nxtVal+"px)) rotateY(-70deg) skewY(9deg)");
		nxtVal+=cardSpaces;
	});

$("#navright").click(function(){
	if($(".active").next().hasClass("slideItems"))
	{
		$(".active").removeClass("active")
			.addClass("prev")
			.attr("elad-translate",middleDistance)
			.next()
			.addClass("active")
			.removeClass("next")
			.removeAttr("style")
			.attr("elad-translate","0");

		$(".next").each(function(){
			var thisTrans = parseInt($(this).attr("elad-translate"))-cardSpaces;
			$(this).css("transform","translateX(calc(-50% + "+thisTrans+"px)) rotateY(-70deg) skewY(9deg)");
			$(this).attr("elad-translate",thisTrans);
			// nxtVal+=cardSpaces;
		});

		$(".prev").each(function(){
			var thisTrans = parseInt($(this).attr("elad-translate"))+cardSpaces;
			$(this).css("transform","translateX(calc(-50% - "+thisTrans+"px)) rotateY(70deg) skewY(-9deg)");
			$(this).attr("elad-translate",thisTrans);
			// nxtVal+=cardSpaces;
		});
	}
});
$("#navleft").click(function(){
	if($(".active").prev().hasClass("slideItems"))
	{
		$(".active").removeClass("active")
			.addClass("next")
			.attr("elad-translate",middleDistance)
			.prev()
			.addClass("active")
			.removeClass("prev")
			.removeAttr("style")
			.attr("elad-translate","0");

		$(".next").each(function(){
			var thisTrans = parseInt($(this).attr("elad-translate"))+cardSpaces;
			$(this).css("transform","translateX(calc(-50% + "+thisTrans+"px)) rotateY(-70deg) skewY(9deg)");
			$(this).attr("elad-translate",thisTrans);
			// nxtVal+=cardSpaces;
		});

		$(".prev").each(function(){
			var thisTrans = parseInt($(this).attr("elad-translate"))-cardSpaces;
			$(this).css("transform","translateX(calc(-50% - "+thisTrans+"px)) rotateY(70deg) skewY(-9deg)");
			$(this).attr("elad-translate",thisTrans);
			// nxtVal+=cardSpaces;
		});
	}
});