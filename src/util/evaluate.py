import csv
import sys 

def evaluate_classifier(classifier, eval_set, batch_size):
    """
    Function to get accuracy and cost of the model, evaluated on a chosen dataset.

    classifier: the model's classfier, it should return genres, logit values, and cost for a given minibatch of the evaluation dataset
    eval_set: the chosen evaluation set, for eg. the dev-set
    batch_size: the size of minibatches.
    """
    correct = 0
    genres, hypotheses, cost = classifier(eval_set)
    cost = cost / batch_size
    full_batch = int(len(eval_set) / batch_size) * batch_size
    for i in range(full_batch):
        hypothesis = hypotheses[i]
        if hypothesis == eval_set[i]['label']:
            correct += 1        
    return correct / float(len(eval_set)), cost

def evaluate_classifier_genre(classifier, eval_set, batch_size):
    """
    Function to get accuracy and cost of the model by genre, evaluated on a chosen dataset. It returns a dictionary of accuracies by genre and cost for the full evaluation dataset.
    
    classifier: the model's classfier, it should return genres, logit values, and cost for a given minibatch of the evaluation dataset
    eval_set: the chosen evaluation set, for eg. the dev-set
    batch_size: the size of minibatches.
    """
    genres, hypotheses, cost = classifier(eval_set)
    correct = dict((genre,0) for genre in set(genres))
    count = dict((genre,0) for genre in set(genres))
    cost = cost / batch_size
    full_batch = int(len(eval_set) / batch_size) * batch_size

    for i in range(full_batch):
        hypothesis = hypotheses[i]
        genre = genres[i]
        if hypothesis == eval_set[i]['label']:
            correct[genre] += 1.
        count[genre] += 1.

        if genre != eval_set[i]['genre']:
            print('welp!')

    accuracy = {k: correct[k]/count[k] for k in correct}

    return accuracy, cost

def evaluate_classifier_bylength(classifier, eval_set, batch_size):
    """
    Function to get accuracy and cost of the model by genre, evaluated on a chosen dataset. It returns a dictionary of accuracies by genre and cost for the full evaluation dataset.
    
    classifier: the model's classfier, it should return genres, logit values, and cost for a given minibatch of the evaluation dataset
    eval_set: the chosen evaluation set, for eg. the dev-set
    batch_size: the size of minibatches.
    """
    genres, hypotheses, cost = classifier(eval_set)
    correct = dict((genre,0) for genre in set(genres))
    count = dict((genre,0) for genre in set(genres))
    cost = cost / batch_size
    full_batch = int(len(eval_set) / batch_size) * batch_size

    for i in range(full_batch):
        hypothesis = hypotheses[i]
        genre = genres[i]
        if hypothesis == eval_set[i]['label']:
            correct[genre] += 1.
        count[genre] += 1.

        if genre != eval_set[i]['genre']:
            print('welp!')

    accuracy = {k: correct[k]/count[k] for k in correct}

    return accuracy, cost

def evaluate_final(classifier, eval_sets, batch_size):
    """
    Function to get percentage accuracy of the model, evaluated on a set of chosen datasets.
    classifier: the model's classfier, it should return genres, logit values, and cost for a given minibatch of the evaluation dataset
    eval_set: the chosen evaluation set, for eg. the dev-set
    batch_size: the size of minibatches.
    """
    percentages = []
    length_results = []
    for eval_set in eval_sets:
        bylength_prem = {}
        bylength_hyp = {}
        genres, hypotheses, cost = classifier(eval_set)
        correct = 0
        cost = cost / batch_size
        full_batch = int(len(eval_set) / batch_size) * batch_size

        for i in range(full_batch):
            hypothesis = hypotheses[i]
            
            length_1 = len(eval_set[i]['sentence1'].split())
            length_2 = len(eval_set[i]['sentence2'].split())
            if length_1 not in bylength_prem.keys():
                bylength_prem[length_1] = [0,0]
            if length_2 not in bylength_hyp.keys():
                bylength_hyp[length_2] = [0,0]

            bylength_prem[length_1][1] += 1
            bylength_hyp[length_2][1] += 1

            if hypothesis == eval_set[i]['label']:
                correct += 1  
                bylength_prem[length_1][0] += 1
                bylength_hyp[length_2][0] += 1    
        percentages.append(correct / float(len(eval_set)))  
        length_results.append((bylength_prem, bylength_hyp))
    return percentages, length_results


def make_predictions(classifier, eval_set, name):
    """Get comma-separated CSV of predictions.
    Output file has two columns: pairID, prediction
    """
    INVERSE_MAP = {
        0: 'entailment',
        1: 'neutral',
        2: 'contradiction'
    }

    hypotheses = classifier(eval_set)
    predictions = []
    
    for i in range(len(eval_set)):
        hypothesis = hypotheses[1][i]
        prediction = INVERSE_MAP[hypothesis]
        pairID = eval_set[i]["pairID"]
        gold_label = eval_set[i]["gold_label"]
        predictions.append((pairID, prediction, gold_label))

    f = open(name + '_predictions.csv', 'wt')
    w = csv.writer(f, delimiter = ',')
    w.writerow(['pairID','prediction', 'gold_label'])
    for example in predictions:
        w.writerow(example)
    f.close()
