library("matlib")

Information <- function(theta, y)
{
  xi = theta[1]
  sigma = theta[2]
  n = length(y);
  I = matrix(0, nrow = 2, ncol = 2);
  
  f = (1 + xi) / n
  
  I[1,1] = 2*sigma*sigma
  I[1,2] = sigma
  I[2,1] = I[1,2]
  I[2,2] = 1 + xi
  #I[1,1] = n * xi * xi;
  #I[1,2] = sum(y/(1 + xi/sigma*y));
  #I[2,1] = I[1,2];
  #I[2,2] = n *sigma * sigma / (xi * xi) - sum((y/(1 + xi/sigma*y))^2*(1/xi + 1));
  
  return(I);
}

Score <- function(theta, y)
{
  xi = theta[1]
  sigma = theta[2]
  n = length(y);
  
  d1 = 1/(xi*xi) * sum(log(1 + xi*y/sigma)) - (1 + 1/xi)*sum(y/sigma*1/(1+xi*y/sigma))
  d2 = -n/sigma + (1 + 1/xi)*sum(xi*y/(sigma*sigma)*1/(1 + xi*y/sigma))
  
  return(rbind(d1, d2))
}

scoring_fit_gdp <- function(y, accuracy, maxIterations)
{
  error = 1e6
  theta <-  rbind(1, 1)
  
  while(error > accuracy)
  {
    theta <- theta + inv(Information(theta, y)) %*% Score(theta, y)
    
    s <- Score(theta, y)
    error <- abs(s[1]^2+s[2]^2)
    iter = iter + 1
   
    #if(iter > maxIterations) break
  }
  
  return(theta)
}


theta_star = scoring_fit_gdp(excess.u10, 1e-6, 10000)
Score(theta_star, excess.u10)
theta_star