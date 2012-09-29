// microcin simulation

// model is a CTMC
ctmc

//-----------------------------------------------------------------------
// modules for the different components

const int MAX_MCC_IN;
const int MAX_MCC_OUT;

const double synthesis_rate;
const double output_rate;
const double input_rate;
const double inactivation_rate;

module microcin
  McCin  : [0..MAX_MCC_IN]  init 0;
  McCout : [0..MAX_MCC_OUT] init 0;
  
  [synthesis]     McCin<MAX_MCC_IN -> synthesis_rate : (McCin'=McCin+1);
  [output]        McCin>0 -> McCin*output_rate : (McCin'=McCin-1) & (McCout'=min(McCout+1, MAX_MCC_OUT));
  //[input]         McCin>0 & McCout>0 -> McCin*input_rate : (McCin'=min(McCin+1, MAX_MCC_IN)) & (McCout'=McCout-1);
  [inactivation]  McCin>0 -> McCin*inactivation_rate : (McCin'=McCin-1);
endmodule

rewards "synthesis"
  [synthesis]     true : 1;
endrewards

//rewards "inactivation"
//  [inactivation]  true : 1;
//endrewards

rewards "time"
  true : 1;
endrewards

rewards "out_over_in"
  McCin>0 : McCout / McCin;
endrewards

rewards "in"
  true : McCin;
endrewards

rewards "out"
  true : McCout;
endrewards
