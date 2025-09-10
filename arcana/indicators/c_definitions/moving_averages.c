#include <math.h>
#include <stdio.h> // for printf
#include "indicators.h"

// nowe data dopisywane na dole df

void sma(const double *data, double *out, const int len, const int period) {
    if (period > len || period < 0) return;

    double sum = 0.0;
    int i;
    for (i = 0;i < period && i < len; i++) {
        sum += data[i];
        out[i] = sum / (i + 1);
    }

    for (; i<len; i++) {
        sum += data[i];
        sum -= data[i - period];
        out[i] = sum / period;
    }
}

void esma(const double *data, double *out, const int len, const int period, const double alpha) {
    if (period > len || period < 0 || alpha < 0.0) return;

    out[0] = data[0];
    for (int i = 1; i < len; i++) {
        out[i] = alpha * data[i] + (1.0 - alpha) * out[i - 1];
    }
}

void ema(const double *data, double *out, const int len, const int period) {
    esma(data, out, len, period, 2.0 / ((double)period + 1.0));
}

void wma(const double *data, double *out, const int len, const int period) {
    // linear time
    // older data hase higher weight; to change it, reverse weights
    if (period > len || period < 0) return;

    double weights[len];
    for (int i=0;i<period;i++) {weights[i]=(double)(i+1);}

    int i;
    double weights_sum;
    double sum;
    for (i=0;i<period-1 && i<len; i++) {
        int cur_period = i+1;

        sum = 0.0;
        weights_sum = 0.0;
        for (int j=0;j<cur_period;j++) {
            sum += weights[j]*data[i-cur_period+1+j];
            weights_sum += weights[j];
        }

        out[i] = sum / weights_sum;
    }

    weights_sum = (double)period*((double)period+1.0)/2.0;

    for (i;i<len;i++) {
        sum = 0.0;
        for (int j=0; j<period; j++) {
            sum += weights[j]*data[i-period+1+j];
        }

        out[i] = sum / weights_sum;
    }
}

void hma(const double *data, double *out, const int len, const int period) {
    if (period > len || period < 0) return;

    double wma_1[len];
    double wma_2[len];
    double wma_3[len];

    wma(data, wma_1, len, floor(period / 2));
    wma(data, wma_2, len, period);
    for (int i=0; i<len; i++) {
        wma_3[i] = 2.0*wma_1[i] - wma_2[i];
    }

    wma(wma_3, out, len, floor(sqrt(period)));
}

void rma(const double *data, double *out, const int len, const int period) {
    if (period > len || period < 0) return;

    esma(data, out, len, period, 1.0/period);
}

void tema(const double *data, double *out, const int len, const int period) {
    if (period > len || period < 0) return;

    double ema_1[len], ema_2[len], ema_3[len];

    ema(data, ema_1, len, period);
    ema(ema_1, ema_2, len, period);
    ema(ema_2, ema_3, len, period);

    for (int i=0; i<len; i++) {
        out[i] = 3.0*ema_1[i] - 3.0*ema_2[i] + ema_3[i];
    }

}

void dema(const double *data, double *out, const int len, const int period) {
    if (period > len || period < 0) return;

    double ema_1[len], ema_2[len];

    ema(data, ema_1, len, period);
    ema(data, ema_2, len, period);

    for (int i=0; i<len; i++) {
        out[i] = 2.0*ema_1[i] - ema_2[i];
    }
}

void kama(const double *data, double *out, const int len, const int period, int n_fast, int n_slow) {
    if (period > len || period < 0 || n_fast < 0 || n_slow < 0 || n_fast > len || n_slow > len) return;
    if (n_fast > n_slow) {
        double temp = n_fast;
        n_fast = n_slow;
        n_slow = temp;
    }

    double sc_fast = 2.0 / (double)(n_fast + 1.0);
    double sc_slow = 2.0 / (double)(n_slow + 1.0);
    double er, sc;

    int i = 0;
    for (i; i<period && i<len; i++) {
        sma(data, out, len, period);
    }

    double denominator;
    for (i; i<len; i++) {
        denominator = 0.0;
        for (int j=0; j<period; j++) {
            denominator += abs(data[i-j] - data[i-j-1]);
        }

        er = abs(data[i] - data[i-period]) / denominator;

        sc = pow(er*(sc_fast-sc_slow) + sc_slow, 2);

        out[i] = out[i-1] + sc*(data[i] - out[i-1]);
    }
}

void frama(const double *data, double *out, const double *high, const double *low, const int len, const int period) {
    if (period <= 0 || period > len) return;

    double D, N, range_1, range_2, alpha, l, h;
    int half;

    for (int t = 0; t < len; t++) {
        if (t < period - 1) {
            sma(data, out, len, period);
        }

        h = high[t - period + 1];
        l = low[t - period + 1];
        for (int i = t - period + 1; i <= t; i++) {
            if (high[i] > h) h = high[i];
            if (low[i]  < l) l = low[i];
        }
        N = h - l;

        half = period / 2;
        h = high[t - period + 1];
        l = low[t - period + 1];
        for (int i = t - period + 1; i < t - period + 1 + half; i++) {
            if (high[i] > h) h = high[i];
            if (low[i]  < l) l = low[i];
        }
        range_1 = h - l;

        h = high[t - half + 1];
        l = low[t - half + 1];
        for (int i = t - half + 1; i <= t; i++) {
            if (high[i] > h) h = high[i];
            if (low[i]  < l) l = low[i];
        }
        range_2 = h - l;

        if (N <= 0.0) {
            D = 0.0;
        } else {
            D = (log(range_1 + range_2) - log(N)) / log(2.0);
        }
        if (D < 1.0) D = 1.0;
        if (D > 2.0) D = 2.0;

        alpha = exp(-4.6 * (D - 1.0));
        if (alpha < 0.01) alpha = 0.01;
        if (alpha > 1.0)   alpha = 1.0;

        if (t == period - 1) {
            double sum = 0.0;
            for (int i = 0; i < period; i++) sum += data[i];
            out[t] = sum / period;
        } else {
            out[t] = alpha * data[t] + (1.0 - alpha) * out[t - 1];
        }
    }
}

