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

// Create the agent.
var create_agent = function() {
  // Setup participant and get node id
  console.log("Create agent called")
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
            submit_response(Wwer1);
            
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

// Submit the answer for this question as an info. 
var submit_response = function(value) {
    clearTimeout(answer_timeout); // This is to stop some bug where it would double submit answers. This stops the timeout.
    $("#countdown").hide();
    data = {
       "contents": value
    }
    dallinger.createInfo(my_node_id, data)
    .done(get_transmissions());
      
}

// Beginning of code for Scorescreen

// Get the participants own participant_ID. Since it is forgotton upon moving pages
var check_ID = function() {
  ID = dallinger.identity.participantId;
  return ID;
}

// Checks for all neighbors of node 1 (the source) with a to connection that are probenodes.
var check_neighbors = function() {
    dallinger.get(
        "/node/" + 2 + "/neighbors",
        {
            connection: "to",
            type: "ProbeNode",
        }
    ).done(function (resp) {
        $("blank").addClass("hidden");
        MYID = check_ID(); // Calls check ID for use in parse_neighbors.
        neighbors = resp.nodes;
        parse_neighbors(neighbors);
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
  console.log("Display score was called");
  $("#Congratulations").show();
  $("#id-head").removeClass("hidden");
  $("#ID").removeClass("hidden");
  $("#ID").html(id);
  $("#other-win").removeClass("hidden");
  $("#Score").removeClass("hidden");
  $("#Score").html(score);
  $("#out-of").removeClass("hidden");
}

// Displays the score when you win.
var display_score_you = function(score , id){
  console.log("Display score you was called");
  $("#Congratulations").show();
  $("#id-head").removeClass("hidden");
  $("#ID").removeClass("hidden");
  $("#ID").html(id);
  $("#you-win").removeClass("hidden");
  $("#Score").removeClass("hidden");
  $("#Score").html(score);
  $("#out-of").removeClass("hidden");
}

// Beginning of code for the PGG page

var start_experiment = function() {
  my_node_id = dallinger.storage.get("my_node"); // Get's the participant's node and saves it
  round = 0 // Set's the round counter, this will increase after each pass
  show_experiment(); 
}

var show_experiment = function() {
  $("#instructions").removeClass("hidden");
  $("#submit-0").removeClass("hidden");
  $("#submit-0").removeClass("disabled");
  $("#submit-1").removeClass("hidden");
  $("#submit-1").removeClass("disabled");
  $("#submit-2").removeClass("hidden");
  $("#submit-2").removeClass("disabled");
  $("#submit-3").removeClass("hidden");
  $("#submit-3").removeClass("disabled");
  $("#submit-4").removeClass("hidden");
  $("#submit-4").removeClass("disabled");
  $("#submit-5").removeClass("hidden");
  $("#submit-5").removeClass("disabled");
  $("#submit-6").removeClass("hidden");
  $("#submit-6").removeClass("disabled");
  $("#submit-7").removeClass("hidden");
  $("#submit-7").removeClass("disabled");
  $("#submit-8").removeClass("hidden");
  $("#submit-8").removeClass("disabled");
  $("#submit-9").removeClass("hidden");
  $("#submit-9").removeClass("disabled");
  $("#submit-10").removeClass("hidden");
  $("#submit-10").removeClass("disabled");
  force_choice = Math.floor(Math.random() * 10) + 0;
  round += 1
  countdown = 10; // Set the desired countdown number here  
  start_experiment_timeout(); 
}

var hide_experiment = function() {
  $("#waiting").removeClass("hidden");
  $("#instructions").addClass("hidden");
  $("#submit-0").addClass("hidden");
  $("#submit-0").addClass("disabled");
  $("#submit-1").addClass("hidden");
  $("#submit-1").addClass("disabled");
  $("#submit-2").addClass("hidden");
  $("#submit-2").addClass("disabled");
  $("#submit-3").addClass("hidden");
  $("#submit-3").addClass("disabled");
  $("#submit-4").addClass("hidden");
  $("#submit-4").addClass("disabled");
  $("#submit-5").addClass("hidden");
  $("#submit-5").addClass("disabled");
  $("#submit-6").addClass("hidden");
  $("#submit-6").addClass("disabled");
  $("#submit-7").addClass("hidden");
  $("#submit-7").addClass("disabled");
  $("#submit-8").addClass("hidden");
  $("#submit-8").addClass("disabled");
  $("#submit-9").addClass("hidden");
  $("#submit-9").addClass("disabled");
  $("#submit-10").addClass("hidden");
  $("#submit-10").addClass("disabled");
}

var start_experiment_timeout = function () {
  console.log("start experiment timeout was called")
  experiment_timeout = setTimeout(function(){
    countdown = countdown - 1;
    console.log(countdown)
    if (countdown <=0) {
      hide_experiment();
      submit_choice(force_choice); // If a participant doesn't decide, a random number is submitted
    } else {
      start_experiment_timeout();
    }
  }, 1000); 
}
                              
var submit_choice = function(value) {
    clearTimeout(experiment_timeout);
    hide_experiment();
    data = {
       "contents": value
    }
    dallinger.createInfo(my_node_id, data)
    .done(get_pog()); // It's like above, only this time it starts checking its neighbors
}

// Get's hold of the pogbot and loops if all nodes haven't chosen yet.
var get_pog = function (){ 
  pog_timeout = setTimeout(function() {
  console.log("Get pog was called")
  dallinger.get(
  "/node/" + my_node_id + "/neighbors",
  {
    connection: "to",
    type: "pot_of_greed_pot",
  }
).done(function (resp){
    pog = resp.nodes
    pog.forEach(function(node){
      id = node.id
      if (id == 2){
        poground = JSON.parse(node.property2).round;
        pot = JSON.parse(node.property1).pot
        if (poground == round) {
          get_results(pot)
        } else {get_pog();
       }
      }
    })
  })
  }, 1000);
}

var get_results = function(pot) {
  clearTimeout(pog_timeout);
  console.log("get results was called")
  pot = parseInt(pot , 10)
  dallinger.get(
        "/node/" + 2 + "/neighbors",
        {
            connection: "to",
            type: "ProbeNode",
        }
     ).done(function (resp) {
    neighbors = resp.nodes;
    check_nodes(neighbors); //Function call
    round_earnings = my_leftovers + pot;
console.log(round_earnings);
    display_results(round_earnings); // function call
  })
}

// Find the leftovers the participant had
var check_nodes = function(neighbors) {
  console.log("check nodes was called")
  neighbors.forEach(function(node) {
    node_id = node.id;
    leftovers = JSON.parse(node.property4).leftovers;
    if (node_id == my_node_id) {
      my_leftovers = leftovers
    }
  })
}

// Show the participant their results
var display_results = function(round_earnings) {
  console.log("display_results was called"); 
  result_countdown = 10; // How long can participants view this?
  $("#waiting").addClass("hidden");
  $("#earnings").removeClass("hidden");
  $("#points").removeClass("hidden"); 
  $("#points").html(round_earnings);
  $("#added").removeClass("hidden");
  start_timer_countdown();  
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
  $("#earnings").addClass("hidden");
  $("#points").addClass("hidden"); 
  $("#added").addClass("hidden");
  if(round < 6){
    show_experiment();
  } else {
    console.log("It's all ogre. Now you just need to build in a submit response and its finished")
  }
}

     

