#ifndef INFERENCE_LINEAR_CONSTRAINT_H__
#define INFERENCE_LINEAR_CONSTRAINT_H__

#include <map>
#include <ostream>

#include "Relation.h"
#include "Solution.h"
/**
 * A sparse linear constraint.
 */
class LinearConstraint {

public:

	LinearConstraint();

	void setCoefficient(unsigned int varNum, double coef);

	void setRelation(Relation relation);

	void setValue(double value);

	const std::map<unsigned int, double>& getCoefficients() const;

	const Relation& getRelation() const;

	double getValue() const;

    bool isViolated(const Solution & solution);

private:

	std::map<unsigned int, double> _coefs;

	Relation _relation;

	double _value;
};

std::ostream& operator<<(std::ostream& out, const LinearConstraint& constraint);

#endif // INFERENCE_LINEAR_CONSTRAINT_H__

