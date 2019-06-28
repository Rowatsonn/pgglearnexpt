var my_node_id;

// Consent to the experiment.
$(document).ready(function() {

  // do not allow user to close or reload
  dallinger.preventExit = true;

  // Print the consent form.
  $("#print-consent").click(function() {
    window.print();
  });

  // Consent to the experiment.
  $("#consent").click(function() {
    store.set("recruiter", dallinger.getUrlParameter("recruiter"));
    store.set("hit_id", dallinger.getUrlParameter("hit_id"));
    store.set("worker_id", dallinger.getUrlParameter("worker_id"));
    store.set("assignment_id", dallinger.getUrlParameter("assignment_id"));
    store.set("mode", dallinger.getUrlParameter("mode"));

    dallinger.allowExit();
    dallinger.goToPage('instructions');
  });

  // Consent to the experiment.
  $("#no-consent").click(function() {
    dallinger.allowExit();
    window.close();
  });

  // Consent to the experiment.
  $("#go-to-experiment").click(function() {
    dallinger.allowExit();
    dallinger.goToPage('exp'); //Make sure we change that 
  });

  $("#submit-response").click(function() {
    $("#submit-response").addClass('disabled');
    $("#submit-response").html('Sending...');
    dallinger.createInfo(my_node_id, {contents: "Submitted", info_type: "Info"})
    .done(function (resp) {
      dallinger.allowExit();
      dallinger.goToPage('questionnaire');
    })
    .fail(function (rejection) {
      dallinger.allowExit();
      dallinger.error(rejection);
    });
  });
});

// Starts a timer to display a new message if participants end up waiting for too long. Implies somebody has gone AFK. 
// This calls in the PGG and the quiz once the participant joins / makes a choice.
var start_AFK_timeout = function(){
  console.log("Start AFK Timeout was called")
  console.log(afk_countdown)
  afk_countdown = afk_countdown- 1
  if (afk_countdown <= 0){
    $("#long_time").show(); // This is a HTML element on both trivia and pgg which just states that participants should keep the window open.
  } 
}
  
// Timer for the popup of the AFK modal on the instructions pages. Timer resets on the HTML code.
var start_modal_timeout = function(counter){
  console.log("modalTimeout was called")
  modal_timeout = setTimeout(function(){
    counter = counter - 1
    console.log("counter is " + counter)
    if (counter <= 0) {
      jQuery.noConflict();
      $('#reading').modal('show');
    } else {
      start_modal_timeout(counter);
    }
  }, 1000);
}


// Create the agent.
var create_agent = function() {
  // Setup participant and get node id
  console.log("Create agent called")
  afk_countdown = 30 // Sets the AFK timeout.
  console.log("afk countdown is " + afk_countdown) 
  $("#submit-response").addClass('disabled');
  dallinger.createAgent()
  .done(function (resp) {
    my_node_id = resp.node.id;
    dallinger.storage.set("my_node" , my_node_id); //This is where we set the cookie for my node
    $("#submit-response").removeClass('disabled');
    get_transmissions(my_node_id); //It starts constantly checking it's transmissions
  })
  .fail(function (rejection) {
    dallinger.allowExit();
    dallinger.error(rejection);
  });
};

// Get a nodes transmissions. This runs constanly once create_agent has run, which it will once you load up the html page 
var get_transmissions = function() {
    console.log("get transmissions was called");
    start_AFK_timeout(); // Starts the timeout in the background for the AFK message to come up
    dallinger.getTransmissions(my_node_id, {
        status: "pending"
    })
    .done(function (resp) {
        transmissions = resp.transmissions;
        console.log(transmissions)
        if (transmissions.length > 0) {
            if (transmissions.length > 1) {
                console.log("More than one transmission - unexpected!");
            } else {
                get_info(transmissions[0].info_id); // This calls the function below. 
            }
        } else {
            setTimeout(function(){
                get_transmissions();
            }, 1000); // Unless the node finds some info, it just calls get_transmissions every second. 
        }
    })
    .fail(function (rejection) {
        console.log(rejection);
        $('body').html(rejection.html);
    });
}

// Get the nodes info. resp is a generic term that servers use for a response from a browser. 
var get_info = function(info_id) {
    $("#long_time").hide();
    afk_countdown = 30 // Resets the AFK timer. Don't want the AFK message popping up unannounced.
    console.log("successfully set the AFK countdown to" + afk_countdown) 
    dallinger.getInfo(my_node_id, info_id)
    .done(function(resp) {
        process_info(resp.info); // This is yet another function call. Also resp, contains an info. 
    })
    .fail(function (rejection) {
        console.log(rejection);
        $('body').html(rejection.html);
    });
}


// Process the info that the node receievs.
var process_info = function(info) {
    parse_question(info);
    if (number == 11) {
        console.log("number identified as 11")
        submit_response(Wwer1); // Creates an info just to signal Q is done. To not break the network again later.
        dallinger.allowExit();
        dallinger.goToPage('score');
    } else {
        display_question(); // This is another function call 
        }
}; 

// This sets the question up ready to be displayed.
var parse_question = function(question) {
    question_json = JSON.parse(question.contents);
    question_text = question_json.question;
    Wwer1 = question_json.Wwer1;
    Wwer2 = question_json.Wwer2
    Rwer = question_json.Rwer;
    number = question_json.number;
}


// Display the question 
var display_question = function() {
    $("#question").html(question_text);
    $("#question_number").html(number);

    var num = Math.random(); 
  
     if (num <0.33) {
       $("#submit-a").html(Rwer);
       if (Math.random() <0.5 ){
           $("#submit-b").html(Wwer1);
           $("#submit-c").html(Wwer2);
           } else {
             $("#submit-b").html(Wwer2);
             $("#submit-c").html(Wwer1); 
           }
     } else if (num >0.33 && num <0.66 ) {
       $("#submit-b").html(Rwer);
       if (Math.random() <0.5 ){
           $("#submit-a").html(Wwer1); 
           $("#submit-c").html(Wwer2);
           } else {
           $("#submit-a").html(Wwer2); 
           $("#submit-c").html(Wwer1);
           }
     } else {
       $("#submit-c").html(Rwer); 
       if (Math.random() <0.5){
         $("#submit-a").html(Wwer1);
         $("#submit-b").html(Wwer2);
       } else {
         $("#submit-a").html(Wwer2);
         $("#submit-b").html(Wwer1);
       }
 }; //End of the if else statement 
    enable_answer_buttons(); //Calls another two functions below
    countdown = 5; // This can set the time they have to answer
    start_answer_timeout();
}; // End of the function

// Start a timer to countdown to when the participant needs to have answered by
var start_answer_timeout = function() {
    $("#countdown").show();
    answer_timeout = setTimeout(function() {
        countdown = countdown - 1;
        $("#countdown").html(countdown);
        if (countdown <= 0) {
            disable_answer_buttons(); // Calls another function
            $("#countdown").hide();
            $("#countdown").html("");
            submit_response(Wwer1, human=false);
        } else {
            start_answer_timeout();
        }
    }, 1000);
}

// Displays and engages the answer buttons
var enable_answer_buttons = function() {
    $("#submit-a").removeClass('disabled');
    $("#submit-b").removeClass('disabled');
    $("#submit-c").removeClass('disabled');
    $("#submit-a").show();
    $("#submit-b").show();
    $("#submit-c").show(); 
}

// Hides and disengages the answer buttons
var disable_answer_buttons = function() {
    $("#submit-a").addClass('disabled');
    $("#submit-b").addClass('disabled');
    $("#submit-c").addClass('disabled');
    $("#submit-a").hide();
    $("#submit-b").hide();
    $("#submit-c").hide();
    $("#question").html("Waiting for the next question..."); 
}

// Submit the answer for this question as an info. Human defaults to true but is passed false if it was chosen by the timer 
var submit_response = function(value, human=true) {
    clearTimeout(answer_timeout); // This is to stop some bug where it would double submit answers. This stops the timeout.
    $("#countdown").hide()
    dallinger.createInfo(my_node_id, {
      contents: value,
      property1: JSON.stringify({
        "human": human
      })
    }).done(get_transmissions());  
}

// Beginning of code for Scorescreen

// Finds and saves the ID of the Pog as a cookie
var save_pog = function(){
  my_node_id = dallinger.storage.get("my_node");
  dallinger.get(
  "/node/" + my_node_id + "/neighbors",
  {
    connection: "to",
    node_type: "PogBot",
  }
).done(function(resp){
    pog = resp.nodes
    console.log(pog)
    if (pog.length > 0){
      pog.forEach(function(node){
        pog_id = node.id
        dallinger.storage.set("pog" , pog_id)
        if (typeof pog_id === "undefined"){
          save_pog();
        } else {
          check_neighbors(pog_id);
        }
      })
    } else {
      save_pog(); // Recalls the function if it doesn't find the pog
    }
  })
}

// Checks what condition it is for the nodes. 
var condition_check = function(pog_id){
  console.log("Condition check was called");
  dallinger.get(
  
  "/node/" + pog_id + "/neighbors",
  {
        connection: "to",
    }
).done(function(resp){
    nodes = resp.nodes;
    console.log(nodes)
    nodes.forEach(function(node){
      node_id = node.id
      condition = JSON.parse(node.property4).info_choice
      console.log("condition is")
      console.log(condition)
      console.log("ID is")
      console.log(node_id)
      console.log("My node ID is")
      console.log(my_node_id)
      if (node_id = my_node_id){
        console.log("Made it to the if statement")
        console.log(condition)
        dallinger.storage.set("my_condition" , condition)
      }
    })
  })
}

// Get the participants own participant_ID. Since it is forgotton upon moving pages
var check_ID = function() {
  ID = dallinger.identity.participantId;
  return ID;
}

var hide_blank = function() {
   $("#blank").hide();
}

// Checks for all neighbors of the pog with a to connection
var check_neighbors = function(pog_id){
    console.log(pog_id)
    dallinger.get(
        "/node/" + pog_id + "/neighbors",
        {
            connection: "to",
        }
    ).done(function (resp) {
        MYID = check_ID(); // Calls check ID for use in parse_neighbors.
        neighbors = resp.nodes;
        console.log(neighbors)
        if (neighbors.length == 0) {
            check_neighbors()
        } else {
        parse_neighbors(neighbors);
        }
    })
  }

// After getting said neighbors. This interprets them.
var parse_neighbors = function(neighbors) {
    neighbors.forEach(function(node) {
    score = JSON.parse(node.property1).score_in_quiz;
    prestige = JSON.parse(node.property2).prestige;
    id = node.participant_id;
    if (prestige == 1 && id == MYID) {
      display_score_you(score, id);
    } else if (prestige == 1) {
      display_score(score, id);
    } 
  });
}

// Displays the score when someone else is the winner
var display_score = function(score , id){
  hide_blank();
  $("#Congratulations").show();
  $("#id-head").removeClass("hidden");
  $("#ID").removeClass("hidden");
  $("#ID").html(id);
  $("#other-win").show();
  $("#Score").removeClass("hidden");
  $("#Score").html(score);
  $("#out-of").removeClass("hidden");
  condition_check(pog_id);
}

// Displays the score when you win.
var display_score_you = function(score , id){
  hide_blank();
  $("#Congratulations").show();
  $("#id-head").removeClass("hidden");
  $("#ID").removeClass("hidden");
  $("#ID").html(id);
  $("#you-win").show();
  $("#Score").removeClass("hidden");
  $("#Score").html(score);
  $("#out-of").removeClass("hidden");
  condition_check(pog_id);
}

// Beginning of code for the PGG instructions

var begin_instructions = function(){
  console.log("Begin instructions was called")
  my_node_id = dallinger.storage.get("my_node");
  ping_server(my_node_id);
  dallinger.get(
  "/node/" + my_node_id + "/neighbors",
  {
    connection: "to",
    node_type: "PogBot",
  }
).done(function(resp) {
    pog = resp.nodes
    console.log(pog)
    pog.forEach(function(node){
      id = node.id
      snowdrift = JSON.parse(node.property3).snowdrift;
      console.log(snowdrift)
      dallinger.storage.set("snowdrift" , snowdrift); // Sets the condition as a cookie
      if(snowdrift == 1){
         console.log("It's a SD")
         $("#SD").show();
         $("#next").show();
      } else {
         console.log("It's a PD")
         $("#PD").show();
         $("#next").show();
      }
      })
    })
}

// Get's the infos for the node as a way to ping the server that they are still there
var ping_server = function(){
  console.log("Server Pinged");
  my_node_id = dallinger.storage.get("my_node");
  dallinger.getInfos(my_node_id)
}

// This calls on every pgg instructions page. A cookie saved before which stores whether or not the game is a snowdrift
// and thus participants will see the appropriate instructions.
var page_check = function(){
  ping_server();
  snowdrift = dallinger.storage.get("snowdrift")
  if(snowdrift == 1){
    $("#SD").show();
    $("#next2").show();
  } else {
    $("#PD").show();
    $("#next").show();
  }
}

// This calls on the final page (pgg_condition_check) to explain what information they will receieve OR to provide them with the opportunity to choose
// their social learning (NOT YET PROGRAMMED OR HTML'd)
var final_page = function(){
  console.log("Final Page was called");
  ping_server();
  condition = dallinger.storage.get("my_condition");
  if (condition == "BB"){
    $("#BB").show()
  } else if(condition == "prestige"){
    $("#prestige").show()
  } else if(condition == "payoff"){
    $("#payoff").show()
  } else if(condition == "conformity"){
    $("#conform").show()
  } else if(condition == "full"){
     $("#full").show()
     $("#fullt").show()
  } else if(condition == "regular"){
     $("#regular").show()
     $("#regulart").show()
  } else if(condition == "extra"){
     $("#extra").show()
     $("#extrat").show()
  }
}

// Beginning of code for the PGG page

var start_experiment = function() {
  afk_countdown = 30 
  my_node_id = dallinger.storage.get("my_node"); // Gets the participant's node and saves it
  pog_id = dallinger.storage.get("pog"); // Gets the pog's ID
  round = 0 // Set's the round counter, this will increase after each pass
  show_experiment(); 
}

var show_experiment = function() {
  for (var i = 0; i < 11; i++){ // For every button on the screen
  button = "#submit-" + i
  $(button).show()
  $(button).removeClass("disabled");
 }
  force_choice = Math.floor(Math.random() * 10) + 0;
  round += 1
  $("#instructions").show();
  countdown = 10; // Set the desired countdown number here  
  start_experiment_timeout(); 
}

var hide_experiment = function() {
for (var i = 0; i < 11; i++){ // For every button on the screen
  button = "#submit-" + i
  $(button).hide()
  $(button).addClass("disabled");
 }
 $("#waiting").show();
 $("#countdown").hide(); // Hides the countdown
 $("#instructions").hide();
}

var start_experiment_timeout = function () {
  console.log("start experiment timeout was called")
  experiment_timeout = setTimeout(function(){
    $("#countdown").show()
    countdown = countdown - 1;
    $("#countdown").html(countdown);
    console.log(countdown)
    if (countdown <=0) {
      hide_experiment();
      submit_choice(force_choice, human=false); // If a participant doesn't decide, a random number is submitted
    } else {
      start_experiment_timeout();
    }
  }, 1000); 
}

//Submits the participants choice. Human defaults to true, unless the choice is random.                               
var submit_choice = function(value, human=true) {
    clearTimeout(experiment_timeout);
    hide_experiment();
    dallinger.createInfo(my_node_id, {
      contents: value,
      property1: JSON.stringify({
        "human": human
      })
    }).done(get_pog()); // It's like above, only this time it starts checking its neighbors
}

// Get's hold of the pogbot and loops if all nodes haven't chosen yet.
var get_pog = function (){ 
  pog_timeout = setTimeout(function() {
  start_AFK_timeout();
  console.log("Get pog was called")
  dallinger.get(
  "/node/" + my_node_id + "/neighbors",
  {
    connection: "to",
    node_type: "PogBot",
  }
).done(function (resp){
    pog = resp.nodes
    console.log(pog)
    pog.forEach(function(node){
      id = node.id
      poground = JSON.parse(node.property2).round;
      pot = JSON.parse(node.property1).pot
      if (poground == round) {
        get_results(pot)
      } else { 
        get_pog();
      }
    })
  })
  }, 1000);
}

// Retrieves the nodes leftovers and the pot and works out how much they earned that round
var get_results = function(pot) {
  console.log("get results was called")
  clearTimeout(pog_timeout);
  afk_countdown = 30 // Resets the AFK timer
  $("#long_time").hide();
  pot = parseInt(pot , 10)
  dallinger.get(
        "/node/" + pog_id + "/neighbors",
        {
            connection: "to",
            type: "ProbeNode",
        }
     ).done(function (resp) {
    neighbors = resp.nodes;
    check_nodes(neighbors); //Function call
    round_earnings = my_leftovers + pot;
    if(round_earnings == 0){ //In SD, if the threshold wasn't met, this will be true.
      fail_round(); // Calls a function to display relevant snowdrift information
    } else {
        display_results(round_earnings); // function call
    }
  })
}

// Find the leftovers the participant had
var check_nodes = function(neighbors) {
  console.log("check nodes was called")
  neighbors.forEach(function(node) { // The block of code below is extracting the relevent social information from the node. It takes the last element in the list.
    node_id = node.id;
    leftovers = JSON.parse(node.property4).leftovers;
    info_choice = JSON.parse(node.property4).info_choice;
    prestige_list = JSON.parse(node.property5).prestige_list;
    last_prestige = prestige_list[prestige_list.length - 1];
    conformity_list = JSON.parse(node.property5).conform_list;
    last_conformity = conformity_list[conformity_list.length - 1];
    payoff_list = JSON.parse(node.property5).payoff_list;
    last_prestige = payoff_list[payoff_list.length - 1];
    if (node_id == my_node_id) {
      my_leftovers = leftovers
      my_info = info_choice // This checks which info the participant needs. This is robust to different choices, which is nice.  
    }
  })
}

// Show the participant their results
var display_results = function(round_earnings) {
  console.log("display_results was called"); 
  result_countdown = 10; // How long can participants view this?
  $("#waiting").hide();
  $("#earnings").show();
  $("#points").show(); 
  $("#points").html(round_earnings);
  $("#added").show();
  if (my_info == "prestige"){
    console.log("My prestige is " + last_prestige)
    $("#donate").show()
    $("#prestige").show()
    $("#donate").html(last_prestige)
  } else if (my_info == "conformity"){
    $("#donate").show()
    $("#conformity").show()
    $("#donate").html(last_conformity)
  } else if (my_info == "payoff"){
    $("#donate").show()
    $("#payoff").show()
    $("#donate").html(last_payoff)
  } else if (my_info == "full"){
    full_info(neighbors) // Calls the function below
  } else if (my_info == "regular"){
    reg_pgg(neighbors) // Calls a similar function to full, without the social learning extras
  } else if (my_info == "extra"){
    extra_info(neighbors) // Calls a copy of full with a column for total score. Had to be done like this because the table wouldn't display otherwise
  }
start_timer_countdown();  
  }

// In the full info condition, this function handles getting the last donation and ID for each participant and putting it on the table. It also identifies the prestigious and the winning node.
var full_info = function(neighbors){
  console.log("full info was called")
  winning_score = 0
  $("#table").show(); // Displays the sentence above the table
  $("#full").show(); // Displays the table without total score
  neighbors.forEach(function(node) {
    node_score = JSON.parse(node.property3).score_in_pgg
    if (node_score > winning_score){
      winning_score = node_score
    }
  })
  var neighborsLength = neighbors.length;
  for (var i = 0; i < neighborsLength; i++){ //For every neighbor
    node = neighbors[i]
    console.log(node);
    ID = node.participant_id;
    donation = JSON.parse(node.property4).donation;
    prestige = JSON.parse(node.property2).prestige;
    score = JSON.parse(node.property3).score_in_pgg;
    if (prestige == 1){
      ID = "***" + ID + "***"
    }
    if (score == winning_score){
      donation = donation + " (This participant currently has the highest score)"
    }
    row_name = "#row" + (i+1);
    $(row_name).show();
    id_name = "#id" + (i+1);
    $(id_name).html(ID);
    donation_name = "#donation" + (i+1);
    $(donation_name).html(donation);
  }
}

// In the extra_info condition. Participants see the same information as in the full_info, only they also get a column specifying each participants current score. 
var extra_info = function(neighbors){
  console.log("extra info was called")
  winning_score = 0
  $("#table").show(); // Displays the sentence above the table
  $("#extra").show(); // Displays the table with total score
  neighbors.forEach(function(node) {
    node_score = JSON.parse(node.property3).score_in_pgg
    if (node_score > winning_score){
      winning_score = node_score
    }
  })
  var neighborsLength = neighbors.length;
  for (var i = 0; i < neighborsLength; i++){ //For every neighbor
    node = neighbors[i]
    console.log(node);
    ID = node.participant_id;
    donation = JSON.parse(node.property4).donation;
    prestige = JSON.parse(node.property2).prestige;
    score = JSON.parse(node.property3).score_in_pgg;
    if (prestige == 1){
      ID = "***" + ID + "***"
    }
    if (score == winning_score){
      donation = donation + " (This participant currently has the highest score)"
    }
    row_name = "#erow" + (i+1);
    $(row_name).show();
    id_name = "#eid" + (i+1);
    $(id_name).html(ID);
    donation_name = "#edonation" + (i+1);
    $(donation_name).html(donation);
    total_score_name = "#etotalscore" + (i+1)
    $(total_score_name).html(score)
  }
}

// In the reg_pgg condition, this function handles getting the last donation and ID for each participant and putting it on the table.
var reg_pgg = function(neighbors){
  console.log("reg pgg was called")
  $("#full").show(); // Displays the table
  $("#table").show(); // Displays the sentence above the table
  var neighborsLength = neighbors.length;
  for (var i = 0; i < neighborsLength; i++){ //For every neighbor
    node = neighbors[i]
    console.log(node);
    ID = node.participant_id;
    donation = JSON.parse(node.property4).donation;
    row_name = "#row" + (i+1);
    $(row_name).show();
    id_name = "#id" + (i+1);
    $(id_name).html(ID);
    donation_name = "#donation" + (i+1);
    $(donation_name).html(donation);
  }
}


// Starts a timer for the scorescreen to keep everyone synced up
var start_timer_countdown = function() {
  console.log("start timer countdown was called")
  results_timeout = setTimeout(function(){
    result_countdown = result_countdown - 1;
    console.log(result_countdown);
    if (result_countdown <=0) {
      hide_results(); 
    } else {
      start_timer_countdown();
    }
  }, 1000);
}

// Hides the results and recalls show expeirment if the rounds aren't finished.
var hide_results = function() {
  clearTimeout(results_timeout);
  console.log("hide results was called")
  $("#earnings").hide();
  $("#points").hide(); 
  $("#added").hide();
  $("#prestige").hide();
  $("#conformity").hide();
  $("#payoff").hide();
  $("#donate").hide();
  $("#full").hide();
  $("#extra").hide();
  $("#table").hide();
  if(round < 6){
    show_experiment();
  } else {
    dallinger.allowExit();
    dallinger.goToPage('questionnaire');
  }
}

// Displays the HTML script telling the participants they scored 0 this round
var fail_round = function(){
  console.log("fail round was called")
  snow_countdown = 10; 
  $("#waiting").hide();
  $("#SD").show();
  $("#SD1").show();
  if (my_info == "prestige"){
    $("#prestige").show()
    $("#donate").show()
    $("#donate").html(last_prestige)
  } else if (my_info == "conformity"){
    $("#conformity").show()
    $("#donate").show()
    $("#donate").html(last_conformity)
  } else if (my_info == "payoff"){
    $("#payoff").show()
    $("#donate").show()
    $("#donate").html(last_payoff)
  } else if (my_info == "full" || my_info == "extra"){
    full_info(neighbors);
  } else if (my_info == "regular"){
    reg_pgg(neighbors) // Calls a similar function to full, without the social learning extras
  } 
  start_snow_countdown();
}

// Starts a countdown to determine how long this is on screen for
var start_snow_countdown = function(){
  console.log("start snow countdown was called")
  snow_timeout = setTimeout(function(){
    snow_countdown = snow_countdown - 1;
    console.log(snow_countdown);
    if(snow_countdown <=0){
      hide_snow();
    } else {
      start_snow_countdown();
    }
  }, 1000);
}

// Hides the snowdrift information and recalls the experiment if the rounds aren't finished.
var hide_snow = function(){
  clearTimeout(snow_timeout);
  console.log("hide snow was called")
  $("#SD").hide();
  $("#SD1").hide();
  $("#prestige").hide();
  $("#conformity").hide();
  $("#payoff").hide();
  $("#donate").hide();
  $("#full").hide();
  $("#extra").hide();
  $("#table").hide();
  if(round < 6){
    show_experiment();
  } else {
    dallinger.allowExit();
    dallinger.goToPage('questionnaire');
  }
}     

