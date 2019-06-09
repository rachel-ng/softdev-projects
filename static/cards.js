var svg_width = c.getAttribute("width");
var card_width = 108.16;
var x_shift = card_width * 1.5;
var stable_shift = 125;

var opponent_y = 0;
var gen_y = 125 + (stable_shift / 2);
var nursery_y = 325 + (stable_shift / 2);
var discard_y = 225 + (stable_shift / 2);
var player_y = 450 + stable_shift;



// shift card deck (i.e. hands, stables) over -- discarding / destroying / sacrificing cards
var shift = function(card_deck) {
  var i;
  for(i = 0; i < card_deck.length; i++) {
    card_deck[i].setAttribute("x", i * card_width + x_shift);
  }
}

// shuffle deck
var shuffle = function(deck) {
  var i, j;
  for(i = deck.length - 1; i > 0; i--) {
    j = Math.floor(Math.random() * (i+1));
    temp = deck[i];
    deck[i] = deck[j];
    deck[j] = temp;
  }
};

// change coordinates of cards
var card_coords = function(card, c_x, c_y) {
  card.setAttribute("x", c_x);
  card.setAttribute("y", c_y);
}

// change dimensions of cards (i.e. when a player hovers over their hand)
var card_dimensions = function(card, c_width, c_height) {
  card.setAttribute("width", c_width);
  card.setAttribute("height",c_height);
}

var make_card = function(name, type, att) {
  // set all the attributes for the cards
  var card = document.createElementNS("http://www.w3.org/2000/svg", "image");
  card.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href", "https://raw.githubusercontent.com/tfabiha/unstablepics/master/back.jpg");
  card_dimensions(card, card_width, 150);
  card_coords(card, 0, gen_y);
  card.setAttribute("name", name);
  card.setAttribute("type", type);
  card.setAttribute("att", att);
  card.setAttribute("player", "f") //set player to false
  card.addEventListener("mouseover", function() {
    // all card alignment
    if (card.getAttribute("player") == "t") { //"t" == true
      card_dimensions(card, card_width * 3, 450);
      card_coords(card, card.getAttribute("x"), player_y - 150);
    }
    var adder = 0
    for (i = 0; i < player_hand.length; i++) {
      player_hand[i].setAttribute("x", card_width * i + adder + x_shift);
      player_hand[i].setAttribute("align", "left");

      if (player_hand[i] == card) {
        adder = card_width * 2;
      }
    }
  });
  card.addEventListener("mouseout", function() {
    // fix card alignment
    if (card.getAttribute("player") == "t") { //"t" == true
      card_dimensions(card, card_width, 150);
      card_coords(card, card.getAttribute("x"), player_y);
    }

    for (i = 0; i < player_hand.length; i++) {
      player_hand[i].setAttribute("x", card_width * i + x_shift);
      player_hand[i].setAttribute("align", "left");
    }
  });
  return card
};

// discard a card
var discard = function(e) {
    // if we are in fact discarding a card
    // this prevents ppl from discarding a card when they're supposed to be, say,
    // playing it on to the stable
    if (mode == "discard" || mode == "discard_effect") 
    {
	var card = e.target; // e is the card that we clicked on
	player_hand = player_hand.filter(function(n) {return n != card}); // remove this card from player's hand

	// this should probably be shift( player_hand )

	// IMAD DID NOT FINISH WRITING DISCARD EFFECT
	
	var i;
	for(i = 0; i < player_hand.length; i++)
	{
	    player_hand[i].setAttribute("x", i * card_width + x_shift);
	}

	card_dimensions(card, card_width, 150);
	card_coords(card, svg_width - card_width, discard_y);
	card.setAttribute("player", "f");
	discard_pile.push(card);

	if (mode == "discard")
	{
	    if (player_hand.length <= 7)
	    {
		mode = "draw";
		turn.innerHTML = "OPPONENT TURN";
		switch_turns();
	    }
	}
	else
	{
	    // this is what's supposed to happen when we discard the opponents
	    // we go through a bunch of stuff and then we change the mode to active
	    // now go back to fxn [ discard_effects ]
	    mode = "activate";
	}
    }
};

//make opponent discard a card
var opponent_discard = function(e) {
  if (mode == "opponent_discard") {
    var card = e.target;
    opponent_stable = opponent_stable.filter(function(n) {return n != card}); // remove this card from opponent's hand

    var i;
    for(i = 0; i < opponent_stable.length; i++) {
      player_hand[i].setAttribute("x", i * card_width + x_shift);
    }

    card_dimensions(card, card_width, 150);
    card_coords(card, svg_width - card_width, discard_y);
    card.setAttribute("player", "f");
    discard_pile.push(card);
    mode = "activate";
  }
}

// play a card
async function play(e) {
  if (mode == "play") {
    var card = e.target;
    player_hand = player_hand.filter(function(n) {return n != card}); // removes the played card from the hand

    var i;
    for(i = 0; i < player_hand.length; i++) {
      player_hand[i].setAttribute("x", i * card_width + x_shift);
    }
    var t = card.getAttribute("type");
    console.log(t);
    if (t == "baby_uni" || t == "basic_uni" || t == "magical_uni") {
      card_dimensions(card, card_width, 150);
      card_coords(card, card.getAttribute("x"), nursery_y);
      card.setAttribute("player", "f");
      player_stable.push(card);
      console.log(card);

      for(i = 0; i < player_stable.length; i++) {
        player_stable[i].setAttribute("x", i * card_width + x_shift);
      }

      if (player_stable.length >= 7) {
        window.location.href = "/win";
      }
    }
    else {
      card_dimensions(card, card_width, 150);
      card_coords(card, svg_width - card_width, discard_y);
      card.setAttribute("player", "f");
      discard_pile.push(card);
      console.log(card);
    }
    mode = "activate";
    if (t == "magical_uni") {
      await activate(card.getAttribute("att"), "uni");
    }
    else if (t == "magic") {
      await activate(card.getAttribute("att"), "magic");
    }
    if (player_hand.length > 7) {
      turn.innerHTML = "DISCARD A CARD";
      mode = "discard";
    }
    else {
      turn.innerHTML = "OPPONENT TURN";
      switch_turns();
      mode = "draw";
    }
  }
}

// only call this fxn if the player is getting rid of some card
async function discard_effect(player)
{
    if (player == "player") // player has to get rid of their own card
    {
	turn.innerHTML = "DISCARD A CARD";

	// changed mode to something else
	// this correlates to a condition in an event listener
	// go to fxn [ discard ] that is where this value for the mode is checked
	mode = "discard_effect";

	// so now that ur back, js isnt going to stop at the previous line
	// it's going to want to continue regardless so we have to figure out to
	// tell it how to wait 
	await check_end();

	// now we have finished waiting for check end
	// our mode rn is == active so we can move on with our lives
	// go to fx [ activate ]
    }
    else // player has to get rid of someone else's card
    {
	if (opponent_stable.length > 0)
	{
	    turn.innerHTML = "DESTROY ONE OF THE OPPONENT'S UNICORN CARDS";
	    mode = "opponent_discard";
	    await check_end();
	}
    }
}

// this fxn says that we promise that at some point the mode
// is going to change to active but until then keep checking to
// see if it's active or not
// when mode == active then u can end the fxn
// so go back to fxn [ discard_effect ]
async function check_end() {
  await new Promise((resolve) => setTimeout(() => {
    if(mode != "activate") {
      return resolve(check_end());
    }else{
      return resolve();
    }
  }, 100));
}

async function activate(att, type) {
  var x = null;
  if (type == "uni") {
    x = JSON.parse(att);
  }
  else {
    x = att.split(',');
    for (var i in x) {
      if (x[i] == "draw") {
        await draw("player"); // calls draw fxn and waits for it to finish running
      }
      if(x[i] == "discard_all") {
          await discard_effect("player"); // calls discard_effect fxn and waits for it to finish running
	  // we have come out of discard_effect finally and we can move on to the
	  // next line of the code
      }
      if(x[i] == "destroy_uni") {
        await discard_effect("opponent"); // calls discard_effect fxn and waits for it to finish running
      }
    }
  }
}

var switch_turns = function() {
  myturn = !myturn;
};

//card_dimensions(card, card_width, 150);
//card_coords(card, card.getAttribute("x"), player_y);
