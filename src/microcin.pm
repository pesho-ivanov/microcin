// microcin simulation

// model is a CTMC
ctmc

//-----------------------------------------------------------------------
// modules for the different components

const int DEATH_LIMIT;
const int MAX_MCC_OUT;

const double synthesis_rate;
const double output_rate;
const double input_rate;
const double inactivation_rate;

module microcin
  McCin  : [0..DEATH_LIMIT]  init 0;
  McCout : [0..MAX_MCC_OUT] init 0;
  
  [synthesis]
    McCin<DEATH_LIMIT
      -> synthesis_rate
        : (McCin' = McCin+1);
  
  [output]
    McCin<DEATH_LIMIT
    & McCin>0
      -> McCin*output_rate
        : (McCin' = McCin<DEATH_LIMIT ? McCin-1 : DEATH_LIMIT)
        & (McCout' = min(McCout+1, MAX_MCC_OUT));
  
  [input]
    McCin<DEATH_LIMIT
    & McCin>0
    & McCout>0
      -> McCout*input_rate
        : (McCin' = min(McCin+1, DEATH_LIMIT))
        & (McCout' = McCout<MAX_MCC_OUT ? McCout-1 : MAX_MCC_OUT);
  
  [inactivation]
    McCin<DEATH_LIMIT
    & McCin>0
      -> McCin*inactivation_rate
        : (McCin' = McCin<DEATH_LIMIT ? McCin-1 : DEATH_LIMIT);
endmodule

rewards "time"
  true : 1;
endrewards

rewards "in"
  true : McCin;
endrewards

rewards "out"
  true : McCout;
endrewards
