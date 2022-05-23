import data_load
import svc
import lp_generate
import lp_solve

def main():
    lp_generate.schedule_real_tasks()

    # The predictions obtained from running the SVM with a high number of bagging estimators
    curves = data_load.read_data("data\\TestingData.txt", "f*")
    predictions = [1.0,1.0,0.0,0.0,1.0,1.0,0.0,1.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,1.0,1.0,1.0,0.0,1.0,0.0,0.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,1.0,1.0,0.0,1.0,0.0,1.0,0.0,1.0,1.0,1.0,0.0,1.0,0.0,0.0,0.0,0.0,1.0,1.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0,0.0,0.0,0.0,1.0,1.0,1.0,0.0,0.0,1.0,0.0]
    svc.save_testing_results(curves, predictions)

    #predictions, curves = svm.predict_testing_data()

    curve_indexes = svc.get_abormal_curves(predictions)
    lp_solve.display_curve_schedules(curve_indexes)

if __name__ == "__main__":
    main()