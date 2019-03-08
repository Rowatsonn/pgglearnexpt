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
  $("#submit-response").addClass('disabled');
  dallinger.createAgent()
  .done(function (resp) {
    my_node_id = resp.node.id;
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
    dallinger.getTransmissions(my_node_id, {
        status: "pending"
    })
    .done(function (resp) {
        transmissions = resp.transmissions;
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
        dallinger.allowExit();
        dallinger.goToPage('scorescreen');
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
    countdown = 15; // This can set the time they have to answer
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

//submit_response still needs to be defined properly

var submit_response = function(value) {
    clearTimeout(answer_timeout); // This is to stop some bug where it would double submit answers. This stops the timeout.
    console.log("Hello " + value)
    data = {
        "contents": value
    }
    dallinger.createInfo(my_node_id, data)
    .done(get_transmissions());
      
}

