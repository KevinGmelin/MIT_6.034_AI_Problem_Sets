from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    goal_tree = OR(hypothesis)
    for rule in rules:
        binding = match(rule.consequent()[0], hypothesis)
        if binding is None:
            continue
        antecedent = populate(rule.antecedent(), binding)
        if isinstance(antecedent, AND):
            sub_goal_tree = AND(map(lambda x: backchain_to_goal_tree(rules, x), antecedent))
            goal_tree.append(sub_goal_tree)
        elif isinstance(antecedent, OR):
            sub_goal_tree = OR(map(lambda x: backchain_to_goal_tree(rules, x), antecedent))
            goal_tree.append(sub_goal_tree)
        else:
            goal_tree.append(backchain_to_goal_tree(rules, antecedent))
    return simplify(goal_tree)


# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
