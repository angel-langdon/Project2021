import { mean } from "@/utils/dataUtils";

export function rSquared(yPred, yReal) {
  let regressionSquaredError = 0;
  let totalSquaredError = 0;
  let yMean = mean(yReal);
  for (let i = 0; i < yPred.length; i++) {
    regressionSquaredError += Math.pow(yReal[i] - yPred[i], 2);
    totalSquaredError += Math.pow(yReal[i] - yMean, 2);
  }
  return 1 - regressionSquaredError / totalSquaredError;
}

export function rmse(yPred, yReal) {
  let regressionSquaredError = 0;
  for (let i = 0; i < yPred.length; i++) {
    regressionSquaredError += Math.pow(yPred[i] - yReal[i], 2);
  }
  return Math.sqrt(regressionSquaredError / yPred.length);
}

export function mae(yPred, yReal) {
  let regressionSquaredError = 0;
  for (let i = 0; i < yPred.length; i++) {
    regressionSquaredError += Math.abs(yPred[i] - yReal[i]);
  }
  return regressionSquaredError / yPred.length;
}
