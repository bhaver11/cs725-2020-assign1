import pandas as pd
import numpy as np
import matplotlib
# matplotlib.use("Agg")
from matplotlib import pyplot as plt

np.random.seed(42)


class Scaler():
    # hint: https://machinelearningmastery.com/standardscaler-and-minmaxscaler-transforms-in-python/
    def __init__(self):
        self.mean = []
        self.std_dev = []
    def __call__(self,features, is_train=False):
        self.mean = np.mean(features,axis=0)
        self.std_dev = np.std(features,axis=0)
        # raise NotImplementedError


def get_features(csv_path,is_train=False,scaler=None,is_test=False):
    '''
    Description:
    read input feature columns from csv file
    manipulate feature columns, create basis functions, do feature scaling etc.
    return a feature matrix (numpy array) of shape m x n 
    m is number of examples, n is number of features
    return value: numpy array
    '''

    '''
    Arguments:
    csv_path: path to csv file
    is_train: True if using training data (optional)
    scaler: a class object for doing feature scaling (optional)
    '''

    '''
    help:
    useful links: 
        * https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        * https://www.geeksforgeeks.org/python-read-csv-using-pandas-read_csv/
    '''

    #from -> https://stackoverflow.com/questions/20517650/how-to-delete-the-last-column-of-data-of-a-pandas-dataframe
    
    if is_test:
        data_frame = pd.read_csv(csv_path)
    else:
        data_frame = pd.read_csv(csv_path, nrows=1) # read just first line for columns
        columns = data_frame.columns.tolist() # get the columns
        cols_to_use = columns[:len(columns)-1] # drop the last one
        data_frame = pd.read_csv(csv_path, usecols=cols_to_use)
    x = data_frame.values #returns a numpy array
    if is_train:
        scaler.__call__(x,is_train)

    x_norm = ((x- scaler.mean)/(scaler.std_dev + 0.000000000000000000001)) #normalize
    x_norm = np.insert(x_norm,0,1,axis=1) ### for adding bias 
    return x_norm
def get_targets(csv_path):
    '''
    Description:
    read target outputs from the csv file
    return a numpy array of shape m x 1
    m is number of examples
    '''
    #from -> https://stackoverflow.com/questions/20517650/how-to-delete-the-last-column-of-data-of-a-pandas-dataframe
    data_frame = pd.read_csv(csv_path, nrows=1) # read just first line for columns
    columns = data_frame.columns.tolist() # get the columns
    cols_to_use = columns[len(columns)-1:]
    df = pd.read_csv(csv_path, usecols=cols_to_use)
    x = df.values #returns a numpy array
    return x

     

def analytical_solution(feature_matrix, targets, C=0.0):
    '''
    Description:
    implement analytical solution to obtain weights
    as described in lecture 4b
    return value: numpy array
    '''

    '''
    Arguments:
    feature_matrix: numpy array of shape m x n
    weights: numpy array of shape m x 1
    '''
    x = feature_matrix
    y = targets
    xt = x.T
    I = np.identity(x.shape[1])  #identity matrix 
    w = np.linalg.inv(xt.dot(x)+C*I).dot(xt.dot(y))
    # w = np.linalg.solve(xt.dot(x) + C ,xt.dot(y))
    return w

def get_predictions(feature_matrix, weights):
    '''
    description
    return predictions given feature matrix and weights
    return value: numpy array
    '''

    '''
    Arguments:
    feature_matrix: numpy array of shape m x n
    weights: numpy array of shape n x 1
    '''
    return feature_matrix.dot(weights)

def mse_loss(predications, targets):
    '''
    Description:
    Implement mean squared error loss function
    return value: float (scalar)
    '''

    '''
    Arguments:
    feature_matrix: numpy array of shape m x n
    weights: numpy array of shape n x 1
    targets: numpy array of shape m x 1
    '''
    mse = (np.square(predications-targets).mean(axis=None))
    return mse

def l2_regularizer(weights):
    '''
    Description:
    Implement l2 regularizer
    return value: float (scalar)
    '''

    '''
    Arguments
    weights: numpy array of shape n x 1
    '''
    return np.linalg.norm(weights)
    # raise NotImplementedError

def loss_fn(feature_matrix, weights, targets, C=0.0):
    '''
    Description:
    compute the loss function: mse_loss + C * l2_regularizer
    '''

    '''
    Arguments:
    feature_matrix: numpy array of shape m x n
    weights: numpy array of shape n x 1
    targets: numpy array of shape m x 1
    C: weight for regularization penalty
    return value: float (scalar)
    '''
    mse = mse_loss(feature_matrix,targets)
    return mse + C*l2_regularizer(weights)
    # raise NotImplementedError

def compute_gradients(feature_matrix, weights, targets, C=0.0):
    '''
    Description:
    compute gradient of weights w.r.t. the loss_fn function implemented above
    '''

    '''
    Arguments:
    feature_matrix: numpy array of shape m x n
    weights: numpy array of shape n x 1
    targets: numpy array of shape m x 1
    C: weight for regularization penalty
    return value: numpy array
    '''
    # print(feature_matrix)
    # print(weights)
    # print(targets)
    loss = (feature_matrix.dot(weights)-targets) 

    # print(loss)

    # cost = np.sum(loss**2)/2*32  + 
    # print(cost)
    # loss = loss_fn(feature_matrix,weights,targets,C)
    # print(feature_matrix.shape[0])
    gradient = (2/feature_matrix.shape[0])*(feature_matrix.T.dot(loss)) + 2.0*C*np.sum(weights)

    # return np.divide(gradient,feature_matrix.shape[0])
    return gradient
    # raise NotImplementedError

def sample_random_batch(feature_matrix, targets, batch_size):
    '''
    Description
    Batching -- Randomly sample batch_size number of elements from feature_matrix and targets
    return a tuple: (sampled_feature_matrix, sampled_targets)
    sampled_feature_matrix: numpy array of shape batch_size x n
    sampled_targets: numpy array of shape batch_size x 1
    '''

    '''
    Arguments:
    feature_matrix: numpy array of shape m x n
    targets: numpy array of shape m x 1
    batch_size: int
    '''    
    # print(feature_matrix.shape)
    rand_indices = np.random.randint(feature_matrix.shape[0], size=batch_size)
    sampled_features = feature_matrix[rand_indices, :]
    sampled_targets = targets[rand_indices,:]
    # print(sampled_features.shape)
    # print(sampled_targets.shape)
    return [sampled_features, sampled_targets]
    # raise NotImplementedError
    
def initialize_weights(n):
    '''
    Description:
    initialize weights to some initial values
    return value: numpy array of shape n x 1
    '''

    '''
    Arguments
    n: int
    '''
    return np.ones((n,1))

def update_weights(weights, gradients, lr):
    '''
    Description:
    update weights using gradient descent
    retuen value: numpy matrix of shape nx1
    '''

    '''
    Arguments:
    # weights: numpy matrix of shape nx1
    # gradients: numpy matrix of shape nx1
    # lr: learning rate
    '''    
    weights = weights - lr*gradients
    return weights
    # raise NotImplementedError

# From -> https://stackoverflow.com/questions/279561/what-is-the-python-equivalent-of-static-variables-inside-a-function
def early_stopping(train_loss):
    last_k_losses.append(train_loss)
    if len(last_k_losses) < k:
        return False
    last_k_losses.pop(0)
    return (max(last_k_losses) - min(last_k_losses)) < min_diff

k = 10 #for early stopping # check last k error values
last_k_losses = []
min_diff = 0.000009


def do_gradient_descent(train_feature_matrix,  
                        train_targets, 
                        dev_feature_matrix,
                        dev_targets,
                        lr=1.0,
                        C=0.0,
                        batch_size=32,
                        max_steps=10000,
                        eval_steps=5):
    '''
    feel free to significantly modify the body of this function as per your needs.
    ** However **, you ought to make use of compute_gradients and update_weights function defined above
    return your best possible estimate of LR weights

    a sample code is as follows --          
    '''
    m,n = train_feature_matrix.shape
    weights = initialize_weights(n)
    dev_loss = mse_loss(dev_feature_matrix.dot(weights), dev_targets)
    train_loss = mse_loss(train_feature_matrix.dot(weights), train_targets)

    print("step {} \t dev loss: {} \t train loss: {}".format(0,dev_loss,train_loss))
    for step in range(1,max_steps+1):

        #sample a batch of features and gradients
        features,targets = sample_random_batch(train_feature_matrix,train_targets,batch_size)
        
        #compute gradients
        gradients = compute_gradients(features, weights, targets, C)
        
        #update weights
        weights = update_weights(weights, gradients, lr)
        
        if step%eval_steps == 0:
            dev_loss = mse_loss(dev_feature_matrix.dot(weights), dev_targets)
            train_loss = mse_loss(train_feature_matrix.dot(weights), train_targets)
            if(early_stopping(train_loss)):
                print('Stopping early')
                return weights
            print("step {} \t dev loss: {} \t train loss: {}".format(step,dev_loss,train_loss))

        '''
        implement early stopping etc. to improve performance.
        '''

    return weights

def do_evaluation(feature_matrix, targets, weights):
    # your predictions will be evaluated based on mean squared error 
    # predictions = get_predictions(feature_matrix, weights)
    predictions = feature_matrix.dot(weights)
    # pred_idx = np.insert(predictions, 0, range(0,predictions.size), axis=1)

    # df = pd.DataFrame(predictions)
    # np.savetxt('pred.csv', pred_idx, delimiter=',', header='instance_id,shares',fmt='%d,%f',comments="")
    # np.savetxt("pred.csv", np.dstack((range(1, predictions.size+1),predictions))[0],"%d,%f",header="instance_id,shares")
    # df.to_csv('test_csv.csv', mode='a', index=True)
    # plt.plot(targets)
    # plt.plot(predictions)
    # plt.show()
    loss =  mse_loss(predictions, targets)
    return loss

if __name__ == '__main__':
    scaler = Scaler() #use of scaler is optional
    train_features, train_targets = get_features('data/train.csv',True,scaler), get_targets('data/train.csv')
    dev_features, dev_targets = get_features('data/dev.csv',False,scaler), get_targets('data/dev.csv')
    
    a_solution = analytical_solution(train_features, train_targets, C=1e-7)
    
    print('evaluating analytical_solution...')
    dev_loss=do_evaluation(dev_features, dev_targets, a_solution)
    train_loss=do_evaluation(train_features, train_targets, a_solution)
    print('analytical_solution \t train loss: {}, dev_loss: {} '.format(train_loss, dev_loss))

    print('training LR using gradient descent...')
    gradient_descent_soln = do_gradient_descent(train_features, 
                        train_targets, 
                        dev_features,
                        dev_targets,
                        lr=0.0002,
                        C=1e-7,
                        batch_size=64,
                        max_steps=6000000,
                        eval_steps=10000)

    print('evaluating iterative_solution...')
    test_features = get_features('data/test.csv',False,scaler,True)
    predictions = get_predictions(test_features,gradient_descent_soln)
    pred_idx = np.insert(predictions, 0, range(0,predictions.size), axis=1)

    np.savetxt('pred.csv', pred_idx, delimiter=',', header='instance_id,shares',fmt='%d,%f',comments="")
    # print(pred_test)
    np.savetxt("soln.csv",a_solution,"%f",delimiter=',')
    dev_loss=do_evaluation(dev_features, dev_targets, gradient_descent_soln)
    train_loss=do_evaluation(train_features, train_targets, gradient_descent_soln)
    print('gradient_descent_soln \t train loss: {}, dev_loss: {} '.format(train_loss, dev_loss))
    


