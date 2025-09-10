#ifdef INDICATORS_H
#define INDICATORS_H

// moving averages
void sma(const double *data, double *out, const int len, const int period);
void esma(const double *data, double *out, const int len, const int period, const double alpha);
void ema(const double *data, double *out, const int len, const int period);
void wma(const double *data, double *out, const int len, const int period);
void hma(const double *data, double *out, const int len, const int period);
void rma(const double *data, double *out, const int len, const int period);
void tema(const double *data, double *out, const int len, const int period);
void dema(const double *data, double *out, const int len, const int period);
void kama(const double *data, double *out, const int len, const int period, const int n_fast, const int n_slow);
void frama(const double *data, double *out, const double *high, const double *low, const int len, const int period);


#endif