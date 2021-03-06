#%%
from typing import overload
from numpy import ndarray
from pandas import DataFrame, read_csv, unique
from matplotlib.pyplot import figure, subplots, savefig, show
from sklearn.neural_network import MLPClassifier
from ds_charts import plot_evaluation_results, multiple_line_chart, horizontal_bar_chart, HEIGHT
from sklearn.metrics import accuracy_score
import sklearn.metrics as metrics


from overfit_knn import AQ_TARGET


#%% 
# TODO FIX ADD RIGHT FILE NAMES
file_tag_air = 'air_quality'
filename_air = 'data/air_quality'
target_air = 'ALARM'

train_air: DataFrame = read_csv(f'{filename_air}_tabular_smote.csv')
trnY_air: ndarray = train_air.pop(target_air).values
trnX_air: ndarray = train_air.values
labels_air = unique(trnY_air)
labels_air.sort()

test_air: DataFrame = read_csv(f'{filename_air}_test.csv')
tstY_air: ndarray = test_air.pop(target_air).values
tstX_air: ndarray = test_air.values

lr_type_air = ['adaptive', 'constant', 'invscaling']
max_iter_air = [100, 300, 500, 750, 1000]
learning_rate_air = [.9, .7, .5, .3, .1]
best_air = ('', 0, 0)
last_best_air = 0
best_model_air = None

#%% 
file_tag_nyc = 'NYC_collisions'
filename_nyc = 'data/NYC_collisions'
target_nyc = 'PERSON_INJURY'

train_nyc: DataFrame = read_csv(f'{filename_nyc}_tabular_smote.csv')
trnY_nyc: ndarray = train_nyc.pop(target_nyc).values
trnX_nyc: ndarray = train_nyc.values
labels_nyc = unique(trnY_nyc)
labels_nyc.sort()

test_nyc: DataFrame = read_csv(f'{filename_nyc}_test.csv')
tstY_nyc: ndarray = test_nyc.pop(target_nyc).values
tstX_nyc: ndarray = test_nyc.values

lr_type_nyc = ['adaptive','constant', 'invscaling']
max_iter_nyc = [100, 300, 500, 750, 1000]
learning_rate_nyc = [.9,.7, .5, .3, .1]
best_nyc = ('', 0, 0)
last_best_nyc = 0
best_model_nyc = None

#%%
def mlp(lr_types, learning_r, max_iter, file_tag, train_X, train_Y, test_X, test_Y, labels, label):
    cols = len(lr_types)
    figure()
    fig, axs = subplots(1, cols, figsize=(cols*HEIGHT, HEIGHT), squeeze=False)
    best = ('', 0, 0)
    last_best = 0
    best_model = None
    
    overfitDone = False # Only the first run, varying the max iter, will be calculated and plotted
    acc_test = []
    acc_train = []
    recall_test = []
    recall_train = []
    
    loss_curves = []
    
    print("mlp starting!")
    for k in range(len(lr_types)):
        print("-learning rate type:",lr_types[k])
        d = lr_types[k]
        values = {}
        for lr in learning_r:
            print("--learning rate:",lr)
            yvalues = []
            
            for n in max_iter:
                print("---max iter:",n)
        
                mlp = MLPClassifier(activation='logistic', solver='sgd', learning_rate=d,
                                    learning_rate_init=lr, max_iter=n, verbose=False)
                mlp.fit(train_X, train_Y)
                prdY = mlp.predict(test_X)
                
                if(n == max(max_iter)):
                    loss_curves.append(mlp.loss_curve_)
                
                acc_tt = accuracy_score(test_Y, prdY)

                if(not overfitDone):
                    rec_tt = metrics.recall_score(test_Y, prdY, average="binary", pos_label=label)
                    
                    prdY_train = mlp.predict(train_X)
                    acc_tr = accuracy_score(train_Y, prdY_train)
                    rec_tr = metrics.recall_score(train_Y, prdY_train, average="binary", pos_label=label)
                    acc_test.append(acc_tt)
                    recall_test.append(rec_tt)
                    acc_train.append(acc_tr)
                    recall_train.append(rec_tr)
                
                yvalues.append(acc_tt)
                
                
                if yvalues[-1] > last_best:
                    best = (d, lr, n)
                    last_best = yvalues[-1]
                    best_model = mlp
            values[lr] = yvalues
            
            overfitDone = True
        multiple_line_chart(max_iter, values, ax=axs[0, k], title=f'MLP with lr_type={d}',
                            xlabel='mx iter', ylabel='accuracy', percentage=True)
        
    savefig(f'images/lab7/mlp/{file_tag}_mlp_study.png')
    show()
    print(f'Best results with lr_type={best[0]}, learning rate={best[1]} and {best[2]} max iter, with accuracy={last_best}')


    prd_trn = best_model.predict(train_X)
    prd_tst = best_model.predict(test_X)
    plot_evaluation_results(labels, train_Y, prd_trn, test_Y, prd_tst)
    savefig(f'images/lab7/mlp/{file_tag}_mlp_best.png')
    show()
    
    figure()
    fig, axs = subplots(1, 1, figsize=(4, 4), squeeze=False)
    
    # print overfit recall
    recall = {"train":recall_train, "test": recall_test}
    multiple_line_chart(max_iter, recall, title='MLP Train and Test Recall', xlabel='n', ylabel='recall', percentage=True)
    print("-- plotted. now saving --")
    savefig(f'images/lab7/mlp/{file_tag}_mlp_overfit_recall_lr0.9_lrtadaptive.png')
    show()
    
    acc = {"train":acc_train, "test": acc_test}
    multiple_line_chart(max_iter, acc, title='MLP Train and Test Accuracy', xlabel='n', ylabel='accuracy', percentage=True)
    print("-- plotted. now saving --")
    savefig(f'images/lab7/mlp/{file_tag}_mlp_overfit_accuracy_lr0.9_lrtadaptive.png')
    show()
    
    # print loss functions
    i = 0
    fig, axs = subplots(1, cols, figsize=(cols*HEIGHT, HEIGHT), squeeze=False)
    print("printing loss functions!")
    for k in range(len(lr_types)):
        losses = {}
        for lr in learning_r:
            losses[lr] = loss_curves[i]
            i += 1
        multiple_line_chart(range(0,max(max_iter)), losses, ax=axs[0, k], title=f'MLP Loss with lr_type={lr_types[k]} and max iter={str(max_iter[-1])}',
                        xlabel='mx iter', ylabel='Loss', percentage=True)
    savefig(f'images/lab7/mlp/{file_tag}_mlp_loss_study.png')
    show()

#%%
mlp(lr_type_air, learning_rate_air, max_iter_air, file_tag_air, trnX_air, trnY_air, tstX_air, tstY_air, labels_air, 'Safe')
#%%
mlp(lr_type_nyc, learning_rate_nyc, max_iter_nyc, file_tag_nyc, trnX_nyc, trnY_nyc, tstX_nyc, tstY_nyc, labels_nyc, 'Injured')